#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Copyright FunASR (https://github.com/alibaba-damo-academy/FunASR). All Rights Reserved.
#  MIT License  (https://opensource.org/licenses/MIT)

import copy
import json
import logging
import os.path
import random
import string
import time

import numpy as np
import torch
from omegaconf import DictConfig, ListConfig
from tqdm import tqdm

from dguard.asr.aliasr.download.download_model_from_hub import download_model
from dguard.asr.aliasr.download.file import download_from_url
from dguard.asr.aliasr.register import tables
from dguard.asr.aliasr.train_utils.load_pretrained_model import load_pretrained_model
from dguard.asr.aliasr.train_utils.set_all_random_seed import set_all_random_seed
from dguard.asr.aliasr.utils import export_utils, misc
from dguard.asr.aliasr.utils.load_utils import load_audio_text_image_video, load_bytes
from dguard.asr.aliasr.utils.misc import deep_update
from dguard.asr.aliasr.utils.timestamp_tools import (
    timestamp_sentence,
    timestamp_sentence_en,
)
from dguard.asr.aliasr.utils.vad_utils import merge_vad, slice_padding_audio_samples

try:
    from dguard.asr.aliasr.models.campplus.cluster_backend import ClusterBackend
    from dguard.asr.aliasr.models.campplus.utils import (
        distribute_spk,
        postprocess,
        sv_chunk,
    )
except:
    pass

# TODO:zhaosheng, only support this functions
from dguard.asr.aliasr.frontends.wav_frontend import WavFrontend # VAD
# model
from dguard.asr.aliasr.models.fsmn_vad_streaming.model import FsmnVADStreaming
# encoder
from dguard.asr.aliasr.models.fsmn_vad_streaming.encoder import FSMN

def prepare_data_iterator(data_in, input_len=None, data_type=None, key=None):
    """ """
    data_list = []
    key_list = []
    filelist = [".scp", ".txt", ".json", ".jsonl", ".text"]

    chars = string.ascii_letters + string.digits
    if isinstance(data_in, str):
        if data_in.startswith("http://") or data_in.startswith("https://"):  # url
            data_in = download_from_url(data_in)

    if isinstance(data_in, str) and os.path.exists(
        data_in
    ):  # wav_path; filelist: wav.scp, file.jsonl;text.txt;
        _, file_extension = os.path.splitext(data_in)
        file_extension = file_extension.lower()
        if file_extension in filelist:  # filelist: wav.scp, file.jsonl;text.txt;
            with open(data_in, encoding="utf-8") as fin:
                for line in fin:
                    key = "rand_key_" + "".join(random.choice(chars) for _ in range(13))
                    if data_in.endswith(
                        ".jsonl"
                    ):  # file.jsonl: json.dumps({"source": data})
                        lines = json.loads(line.strip())
                        data = lines["source"]
                        key = data["key"] if "key" in data else key
                    else:  # filelist, wav.scp, text.txt: id \t data or data
                        lines = line.strip().split(maxsplit=1)
                        data = lines[1] if len(lines) > 1 else lines[0]
                        key = lines[0] if len(lines) > 1 else key

                    data_list.append(data)
                    key_list.append(key)
        else:
            if key is None:
                # key = "rand_key_" + "".join(random.choice(chars) for _ in range(13))
                key = misc.extract_filename_without_extension(data_in)
            data_list = [data_in]
            key_list = [key]
    elif isinstance(data_in, (list, tuple)):
        if data_type is not None and isinstance(
            data_type, (list, tuple)
        ):  # mutiple inputs
            data_list_tmp = []
            for data_in_i, data_type_i in zip(data_in, data_type):
                key_list, data_list_i = prepare_data_iterator(
                    data_in=data_in_i, data_type=data_type_i
                )
                data_list_tmp.append(data_list_i)
            data_list = []
            for item in zip(*data_list_tmp):
                data_list.append(item)
        else:
            # [audio sample point, fbank, text]
            data_list = data_in
            key_list = []
            for data_i in data_in:
                if isinstance(data_i, str) and os.path.exists(data_i):
                    key = misc.extract_filename_without_extension(data_i)
                else:
                    if key is None:
                        key = "rand_key_" + "".join(
                            random.choice(chars) for _ in range(13)
                        )
                key_list.append(key)

    else:  # raw text; audio sample point, fbank; bytes
        if isinstance(data_in, bytes):  # audio bytes
            data_in = load_bytes(data_in)
        if key is None:
            key = "rand_key_" + "".join(random.choice(chars) for _ in range(13))
        data_list = [data_in]
        key_list = [key]

    return key_list, data_list


class VAD_FSMN:
    def __init__(self, **kwargs):
        log_level = getattr(logging, kwargs.get("log_level", "INFO").upper())
        logging.basicConfig(level=log_level)
        model, kwargs = self.build_model(**kwargs)
        self.model = model
        self.kwargs = kwargs
        self.model_path = kwargs.get("model_path")

    @staticmethod
    def build_model(**kwargs):
        set_all_random_seed(kwargs.get("seed", 0))
        device = kwargs.get("device", "cuda")
        if not torch.cuda.is_available() or kwargs.get("ngpu", 1) == 0:
            device = "cpu"
            kwargs["batch_size"] = 1
        kwargs["device"] = device
        torch.set_num_threads(kwargs.get("ncpu", 4))

        # build frontend
        
        frontend_class = WavFrontend
        frontend = frontend_class(**kwargs.get("frontend_conf", {}))
        kwargs["frontend"] = frontend
        # build model
        # model_class = tables.model_classes.get(kwargs["model"])
        model_class = SenseVoiceSmall
        assert model_class is not None, f'{kwargs["model"]} is not registered'
        model_conf = {}
        deep_update(model_conf, kwargs.get("model_conf", {}))
        deep_update(model_conf, kwargs)
        model = model_class(**model_conf)

        # init_param
        init_param = kwargs.get("init_param", None)
        if init_param is not None:
            if os.path.exists(init_param):
                logging.info(f"Loading pretrained params from {init_param}")
                load_pretrained_model(
                    model=model,
                    path=init_param,
                    ignore_init_mismatch=kwargs.get("ignore_init_mismatch", True),
                    oss_bucket=kwargs.get("oss_bucket", None),
                    scope_map=kwargs.get("scope_map", []),
                    excludes=kwargs.get("excludes", None),
                )
            else:
                print(f"error, init_param does not exist!: {init_param}")

        # fp16
        if kwargs.get("fp16", False):
            model.to(torch.float16)
        elif kwargs.get("bf16", False):
            model.to(torch.bfloat16)
        model.to(device)

        if not kwargs.get("disable_log", True):
            tables.print()

        return model, kwargs

    def __call__(self, *args, **cfg):
        kwargs = self.kwargs
        deep_update(kwargs, cfg)
        res = self.model(*args, kwargs)
        return res

    def inference(
        self, input, input_len=None, model=None, kwargs=None, key=None, **cfg
    ):
        kwargs = self.kwargs if kwargs is None else kwargs
        if "cache" in kwargs:
            kwargs.pop("cache")
        deep_update(kwargs, cfg)
        model = self.model if model is None else model
        model.eval()

        batch_size = kwargs.get("batch_size", 1)
        # if kwargs.get("device", "cpu") == "cpu":
        #     batch_size = 1

        key_list, data_list = prepare_data_iterator(
            input, input_len=input_len, data_type=kwargs.get("data_type", None), key=key
        )

        speed_stats = {}
        asr_result_list = []
        num_samples = len(data_list)
        disable_pbar = self.kwargs.get("disable_pbar", False)
        pbar = (
            tqdm(colour="blue", total=num_samples, dynamic_ncols=True)
            if not disable_pbar
            else None
        )
        time_speech_total = 0.0
        time_escape_total = 0.0
        for beg_idx in range(0, num_samples, batch_size):
            end_idx = min(num_samples, beg_idx + batch_size)
            data_batch = data_list[beg_idx:end_idx]
            key_batch = key_list[beg_idx:end_idx]
            batch = {"data_in": data_batch, "key": key_batch}

            if (end_idx - beg_idx) == 1 and kwargs.get(
                "data_type", None
            ) == "fbank":  # fbank
                batch["data_in"] = data_batch[0]
                batch["data_lengths"] = input_len

            time1 = time.perf_counter()
            with torch.no_grad():
                res = model.inference(**batch, **kwargs)
                if isinstance(res, (list, tuple)):
                    results = res[0] if len(res) > 0 else [{"text": ""}]
                    meta_data = res[1] if len(res) > 1 else {}
            time2 = time.perf_counter()

            asr_result_list.extend(results)

            # batch_data_time = time_per_frame_s * data_batch_i["speech_lengths"].sum().item()
            batch_data_time = meta_data.get("batch_data_time", -1)
            time_escape = time2 - time1
            speed_stats["load_data"] = meta_data.get("load_data", 0.0)
            speed_stats["extract_feat"] = meta_data.get("extract_feat", 0.0)
            speed_stats["forward"] = f"{time_escape:0.3f}"
            speed_stats["batch_size"] = f"{len(results)}"
            speed_stats["rtf"] = f"{(time_escape) / batch_data_time:0.3f}"
            description = f"{speed_stats}, "
            if pbar:
                pbar.update(end_idx - beg_idx)
                pbar.set_description(description)
            time_speech_total += batch_data_time
            time_escape_total += time_escape

        if pbar:
            # pbar.update(1)
            pbar.set_description(f"rtf_avg: {time_escape_total/time_speech_total:0.3f}")
        torch.cuda.empty_cache()
        return asr_result_list
