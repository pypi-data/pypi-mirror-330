# coding = utf-8
# @Time    : 2024-05-21  09:02:30
# @Author  : zhaosheng@lyxxkj.com.cn
# @Describe: Dguard Model.

import base64
import uuid
import os
import numpy as np
import torch
import torchaudio
from tqdm import tqdm

from dguard.interface.models_info import model_info as MI
from dguard.speaker.diar.extract_emb import subsegment
from dguard.speaker.diar.make_rttm import merge_segments
from dguard.speaker.diar.spectral_clusterer import cluster
from dguard.speaker.utils.utils import set_seed
from dguard.utils import logger
from dguard.utils.dguard_model_utils import (
    ALL_MODELS,
    DGUARD_MODEL_PATH,
    download_or_load,
    load_model_tiny_model,
    load_wav,
    remove_file,
)
from dguard.vad.dguard_vad import VAD


class DguardModel:
    def __init__(
        self,
        embedding_model_names="dguard_sv_r101_cjsd8000_split_lm",
        device="cpu",
        length=-1,
        max_split_num=5,
        start_time=0,
        mean=False,
        verbose=False,
        channel=0,
        # vad
        apply_vad=False,
        vad_min_duration=0.25,
        vad_smooth_threshold=0.25,
        save_vad_path=None,
        # diar
        diar_num_spks=None,
        diar_min_num_spks=1,
        diar_max_num_spks=20,
        diar_min_duration=0.255,
        diar_window_secs=1.5,
        diar_period_secs=0.75,
        diar_frame_shift=10,
        diar_batch_size=None,
        diar_subseg_cmn=True,
        diar_max_split_num=999,
        seed=42,
        key=None,
    ):
        set_seed(seed)
        # self.key = key
        self.verify(key)
        self.length = length
        self.start_time = start_time
        self.mean = mean
        self.verbose = verbose
        self.save_vad_path = save_vad_path
        self.channel = channel
        self.diar_max_split_num = diar_max_split_num
        self.min_duration = vad_min_duration
        self.smooth_threshold = vad_smooth_threshold
        # Init models
        embedding_models = []
        embedding_sizes = []
        sample_rate = 16000
        feature_extractor = None
        feature_extractors = []
        wavform_normalizes = []
        self.same_feature_extractor = False
        self.same_wavform_normalizes = False
        loaders = []
        if isinstance(embedding_model_names, str):
            if "," in embedding_model_names:
                embedding_model_names = embedding_model_names.split(",")
            else:
                embedding_model_names = [embedding_model_names]
        self.embedding_model_names = embedding_model_names
        if "cuda" not in device and "npu" not in device and (diar_batch_size is None):
            diar_batch_size = 4
            self.echo(f"Set diar_batch_size to {diar_batch_size} because of CPU.")
        if diar_batch_size is None:
            diar_batch_size = 2
            self.echo(f"Set diar_batch_size to {diar_batch_size} because of GPU.")
        assert (
            len(embedding_model_names) > 0
        ), "Dguard Error: At least one model should be provided."
        for model_name in embedding_model_names:
            if isinstance(model_name, dict):
                pt_path = model_name.get("pt", None)
                yaml_path = model_name.get("yaml", None)
                embedding_size = int(model_name["embedding_size"])
                embedding_sizes.append(embedding_size)
                sample_rate = int(model_name.get("sample_rate", 16000))
                feat_dim = int(model_name.get("feat_dim", 80))
                wavform_normalize = model_name.get("wavform_normalize", False)
                loader = model_name.get("mode", "wespeaker")
                model_name = model_name["model"]
            else:
                if model_name not in MI:
                    raise ValueError(
                        f"Dguard Error: Model {model_name} not found in Dguard Default Models."
                    )
                _info = MI[model_name]
                loader = _info.get("mode", "wepeaker")
                pt_path = f"{DGUARD_MODEL_PATH}/{model_name}.pt"
                if not os.path.exists(pt_path):
                    pt_path = _info.get("pt", None)
                    if not pt_path:
                        raise ValueError(
                            f"Dguard Error: Model ckpt {model_name} not found in {DGUARD_MODEL_PATH}."
                            + f"\nLoad {model_name} from {pt_path} failed."
                        )
                pt_path = download_or_load(pt_path, model_name, ext=".pt")
                yaml_path = f"{DGUARD_MODEL_PATH}/{model_name}.yaml"
                if not os.path.exists(yaml_path):
                    print(f"Load {model_name} from {yaml_path} failed.")
                    yaml_path = _info.get("yaml", None)
                    if not yaml_path:
                        raise ValueError(
                            f"Dguard Error: Model yaml {model_name} not found in {DGUARD_MODEL_PATH}."
                            + f"\nLoad {model_name} from {yaml_path} failed."
                        )
                yaml_path = download_or_load(yaml_path, model_name, ext=".yaml")
                embedding_size = int(_info["embedding_size"])
                embedding_sizes.append(embedding_size)
                sample_rate = int(_info["sample_rate"])
                feat_dim = int(_info.get("feat_dim", 80))
                wavform_normalize = _info.get("wavform_normalize", False)

            strict = True
            embedding_model, feature_extractor, key = load_model_tiny_model(
                loader,
                pt_path,
                yaml_path,
                strict,
                device,
                sample_rate,
                feat_dim,
                True,
                key=self.key,
            )
            if key is not None:
                self.key = key
            embedding_models.append(embedding_model)
            feature_extractors.append(feature_extractor)
            wavform_normalizes.append(wavform_normalize)
            loaders.append(loader)

        # check if all loaders are the same
        if len(set(loaders)) == 1:
            self.echo(
                "All loaders are the same , so we use the same feature extractor."
            )
            self.same_feature_extractor = True
        else:
            raise ValueError(
                f"Dguard Error: All loaders should be the same, but got {loaders}"
            )
        if len(set(wavform_normalizes)) == 1:
            self.echo(
                "All wavform_normalizes are the same , so we use the same wavform normalize."
            )
            self.same_wavform_normalizes = True
        else:
            raise ValueError(
                f"Dguard Error: All wavform_normalizes should be the same, but got {wavform_normalizes}"
            )
        self.feature_extractors = feature_extractors
        self.wavform_normalizes = wavform_normalizes
        self.feature_extractor = self.feature_extractors[0]
        self.wavform_normalize = self.wavform_normalizes[0]
        self.vad = VAD()
        self.embedding_models = embedding_models
        self.embedding_sizes = embedding_sizes
        self.sample_rate = sample_rate
        self.max_split_num = max_split_num
        self.device = device
        self.table = {}
        # diarization parmas
        self.apply_vad = apply_vad
        self.diar_num_spks = diar_num_spks
        self.diar_min_num_spks = diar_min_num_spks
        self.diar_max_num_spks = diar_max_num_spks
        self.diar_min_duration = diar_min_duration
        self.diar_window_secs = diar_window_secs
        self.diar_period_secs = diar_period_secs
        self.diar_frame_shift = diar_frame_shift
        self.diar_batch_size = diar_batch_size
        self.diar_subseg_cmn = diar_subseg_cmn
        self.echo(f"* Using Default Model Path: {DGUARD_MODEL_PATH}")

    def verify(self, key=None):
        if key is None:
            self.key = None
        else:
            key = key + "a" * (32 - len(key)) if len(key) < 32 else key[:32]
            key = base64.urlsafe_b64encode(key.encode())
            self.key = key

    def echo(self, text):
        if self.verbose:
            logger.info(text)

    def get_embedding_from_models(self, feat):
        # _tmp_embs = []
        result = {}
        for _index, embedding_model in enumerate(self.embedding_models):
            with torch.no_grad():
                feat = feat.to(self.device)
                emb = embedding_model(feat)
            emb = emb[-1] if isinstance(emb, tuple) else emb
            emb = emb.reshape(-1)
            # Normalize
            emb = emb / torch.norm(emb, p=2)
            assert (
                emb.shape[0] == self.embedding_sizes[_index]
            ), f"Model {self.embedding_model_names[_index]}: {emb.shape[0]} != {self.embedding_sizes[_index]}"
            result[self.embedding_model_names[_index]] = emb
        # result = torch.cat(_tmp_embs, dim=0)
        return result

    def encode(self, wav_file=None, channel=None, detail=False, use_energy_vad=False, data=None, sr=None):
        length = self.length
        mean = self.mean
        if self.apply_vad:
            if data is not None and sr is not None:
                r = self.vad_file(
                    data=data, sr=sr, use_energy_vad=use_energy_vad
                )

            else:
                if not wav_file:
                    raise ValueError("wav_file is None")
                self.echo(f"Load {wav_file} with VAD")
                r = self.vad_file(
                    wav_file, channel, use_energy_vad=use_energy_vad
                )  # Already consider the channel & start time
            wav_data, sr, _ = r["pcm"], r["sample_rate"], r["segments"]
        else:
            if data is not None and sr is not None:
                self.echo(f"Load {wav_file} without VAD")
                wav_data = data
                if len(wav_data.shape) != 1:
                    wav_data = wav_data.reshape(-1)
            else:
                if not wav_file:
                    raise ValueError("wav_file is None")
                self.echo(f"Load {wav_file} without VAD")
                wav_data, sr = load_wav(
                    wav_file,
                    sr=self.sample_rate,
                    channel=self.channel if channel is None else channel,
                    wavform_normalize=self.wavform_normalize,
                    start_time=self.start_time,
                )
        if sr != self.sample_rate:
            self.echo(f"Warning: {wav_file} sample rate is {sr}, not {self.sample_rate}")
            raise ValueError(f"Sample rate {sr} is not supported, please use {self.sample_rate}")
        wav_data.to(torch.float32)
        raw_length = wav_data.shape[1] / sr
        if raw_length < length:
            self.echo(
                f"Warning: {wav_file} is too short, length: {raw_length} is less than {length}"
            )
            length = raw_length
        if length < 0:
            split_num = 1
            tiny_length = raw_length * sr
        else:
            split_num = int(raw_length / length)
            tiny_length = length * sr  # samples
        self.echo(
            f"Split {wav_file} into {split_num} parts, RAW length: {raw_length*sr}(samples), {raw_length}(s), TINY length: {tiny_length}(samples)"
        )
        feats = []
        # for split_index in tqdm(range(split_num)):
        for split_index in range(split_num):
            if split_index == self.max_split_num:
                break
            now_start = int(split_index * tiny_length)
            now_end = int((split_index + 1) * tiny_length)
            wav_data_now = wav_data.clone()[:, now_start:now_end]
            wav_data_now = wav_data_now.to(torch.float32)
            feat = self.feature_extractor(wav_data_now)
            feat = feat.unsqueeze(0)  # [1,feat_dim,time]
            feats.append(feat)
        _tmp_embs = []
        self.echo(f"Get total # of feats: {len(feats)}")
        # for feat in tqdm(feats):
        for feat in feats:
            emb_dict = self.get_embedding_from_models(feat)
            if not mean:
                # self.echo(f"  # Get emb from 1st split, shape: {emb.shape}")
                self.echo(f"  # Tiny length: {tiny_length}")
                if detail:
                    return {
                        "emb": emb_dict,
                        "embs": [emb_dict],
                    }
                else:
                    return emb_dict
            else:
                self.echo(f"  # Get emb only from 1st split")
                _tmp_embs.append(emb_dict)
        # get mean dict
        # mean_emb = torch.stack(_tmp_embs).mean(0)
        result = {}
        for k in emb_dict.keys():
            # get mean emb for this key
            embs = [item[k] for item in _tmp_embs]
            mean_emb = torch.stack(embs).mean(0)
            result[k] = mean_emb
            
        # self.echo(f"mean_emb shape: {mean_emb.shape}")
        self.echo(
            f"  # Get mean emb from {min(self.max_split_num,split_num)} splits" # , shape: {mean_emb.shape}
        )
        self.echo(f"  # Tiny length: {tiny_length}")
        if detail:
            return {
                "emb": result,
                "embs": _tmp_embs,
            }
        else:
            return result

    def encode_list(self, wav_files, channel=None, detail=False, use_energy_vad=False):
        result = []
        for wav in wav_files:
            result.append(self.encode(wav, channel, detail, use_energy_vad))
        return result

    def cosine_similarity(self, e1, e2, need_normalize=False):
        if isinstance(e1, dict) and isinstance(e2, dict):
            assert len(e1) == len(e2), "Length of embeddings should be the same"
            scores = []
            for model_name in e1.keys():
                assert model_name in e2, f"Model {model_name} not found in e2"
                e1_now = e1[model_name]
                e2_now = e2[model_name]
                if not isinstance(e1_now, torch.Tensor):
                    e1_now = torch.tensor(e1_now)
                if not isinstance(e2_now, torch.Tensor):
                    e2_now = torch.tensor(e2_now)
                e1_now = e1_now.to(torch.float32)
                e2_now = e2_now.to(torch.float32)
                assert e1_now.shape == e2_now.shape, f"Shape of {model_name} should be the same"
                if need_normalize:
                    e1_now = e1_now / torch.norm(e1_now, p=2)
                    e2_now = e2_now / torch.norm(e2_now, p=2)
                cosine_score = torch.dot(e1_now, e2_now)
                cosine_score = cosine_score.item()
                scores.append(cosine_score)
                self.echo(f"    -> Model {model_name}: {cosine_score}")
            mean_scores = sum(scores) / len(scores)
            return mean_scores
        # now e1 and e2 are both dict
        if not isinstance(e1, torch.Tensor):
            e1 = torch.tensor(e1)
        if not isinstance(e2, torch.Tensor):
            e2 = torch.tensor(e2)
        e1 = e1.to(torch.float32)
        e2 = e2.to(torch.float32)
        if need_normalize:
            e1 = e1 / torch.norm(e1, p=2)
            e2 = e2 / torch.norm(e2, p=2)
        assert e1.shape == e2.shape
        score = torch.dot(e1, e2)
        score = score.item()
        return score
        # assert e1.shape == e2.shape
        # all_scores = []
        # result = {"scores": {}}
        # start = 0
        # for _index, embedding_size in enumerate(self.embedding_sizes):
        #     e1_now = e1[start : start + embedding_size]
        #     e2_now = e2[start : start + embedding_size]
        #     start += embedding_size
        #     if need_normalize:
        #         e1_now = e1_now / torch.norm(e1_now, p=2)
        #         e2_now = e2_now / torch.norm(e2_now, p=2)
        #     cosine_score = torch.dot(e1_now, e2_now)
        #     cosine_score = cosine_score.item()
        #     # TODO: Normalize the cosine_score to [0,1]
        #     # cosine_score = (cosine_score + 1.0) / 2.0
        #     self.echo(
        #         f"    -> Model {self.embedding_model_names[_index]}: {cosine_score}"
        #     )
        #     all_scores.append(cosine_score)
        #     result["scores"][self.embedding_model_names[_index]] = cosine_score
        # mean_scores = sum(all_scores) / len(all_scores)
        # result["mean_score"] = mean_scores
        return result

    def cosine_similarity_list(self, embeddings1, embeddings2):
        assert len(embeddings1) == len(
            embeddings2
        ), "Length of embeddings should be the same"
        result = []
        for e1, e2 in zip(embeddings1, embeddings2):
            result.append(self.cosine_similarity(e1, e2))
        return result

    def file_similarity(self, wav1, wav2, id1=None, id2=None, use_energy_vad=False):
        if id1 is not None:
            if id1 in self.table:
                e1 = self.table[id1]
            else:
                e1 = self.encode(wav1, use_energy_vad=use_energy_vad)
                self.table[id1] = e1
        else:
            e1 = self.encode(wav1)
        if id2 is not None:
            if id2 in self.table:
                e2 = self.table[id2]
            else:
                e2 = self.encode(wav2, use_energy_vad=use_energy_vad)
                self.table[id2] = e2
        else:
            e2 = self.encode(wav2)
        return self.cosine_similarity(e1, e2)

    def file_similarity_list(self, trial_list, use_energy_vad=False):
        result = []
        # trial: (wav1, wav2, id1, id2)
        for trial in trial_list:
            if len(trial) == 2:
                trial.append(None)
                trial.append(None)
            assert (
                len(trial) == 4
            ), f"Trial {trial} is not valid, Please check the format, Make sure it is [wav1, wav2, id1, id2]"
            result.append(self.file_similarity(trial[0], trial[1], trial[2], trial[3], use_energy_vad))
        return result

    def vad_file(self, audio_path=None, channel=0, use_energy_vad=False, data=None, sr=None):
        min_duration = self.min_duration
        smooth_threshold = self.smooth_threshold
        if data is not None and sr is not None:
            if len(data.shape) != 1 and data.shape[0] != 1:
                data = data[self.channel, :]
            if len(data.shape) == 1:
                data = data.reshape(1, -1)
            pcm = data
            sample_rate = sr
            tmp_audio_path = None
            if sr != self.sample_rate:
                raise ValueError(f"Sample rate {sr} is not supported, please use {self.sample_rate}")
        else:
            if not audio_path:
                raise ValueError("audio_path is None")
            audio_save_name = os.path.basename(audio_path).split(".")[0]
            now_uuid = str(uuid.uuid1())
            # assert {DGUARD_MODEL_PATH}/tmp exists, if not, create it
            if not os.path.exists(f"{DGUARD_MODEL_PATH}/tmp"):
                os.makedirs(f"{DGUARD_MODEL_PATH}/tmp", exist_ok=True)
            tmp_audio_path = f"{DGUARD_MODEL_PATH}/tmp/{audio_save_name}_{now_uuid}_channel{self.channel}.wav"

            pcm, sample_rate = load_wav(
                audio_path,
                sr=self.sample_rate,
                channel=channel if channel is not None else self.channel,
                wavform_normalize=False,
                saveto=tmp_audio_path,
                start_time=self.start_time,
            )
            self.echo(
                f"Before VAD: {pcm.shape}, sample_rate: {sample_rate}, length: {pcm.shape[1]/sample_rate:.2f}"
            )
        # 1. vad
        # try:
        if use_energy_vad:
            # vad_segments = self.vad.get_speech_timestamps_energy(
            #     tmp_audio_path, return_seconds=True
            # )
            vad_segments = self.vad.get_speech_timestamps_energy(
                data=pcm, sample_rate=sample_rate, return_seconds=True)
        else:
            # vad_segments = self.vad.get_speech_timestamps(
            #     tmp_audio_path, return_seconds=True
            # )
            vad_segments = self.vad.get_speech_timestamps(
                data=pcm, sample_rate=sample_rate, return_seconds=True)
        # except Exception as e:
        #     logger.error(f"VAD failed: {e}")
        #     vad_segments = []
        #     remove_file(tmp_audio_path)
        #     return {
        #         "pcm": None,
        #         "sample_rate": sample_rate,
        #         "segments": vad_segments,
        #     }
        # 2. sort
        vad_segments = sorted(vad_segments, key=lambda x: x["start"])
        # 3. merge
        segments = []
        for item in vad_segments:
            begin, end = item["start"], item["end"]
            if smooth_threshold >= 0:
                if len(segments) == 0:
                    segments.append(item)
                else:
                    last_end = segments[-1]["end"]
                    if begin - last_end < smooth_threshold:
                        segments[-1]["end"] = end
                    else:
                        segments.append(item)
            else:
                segments.append(item)
        self.echo(f"VAD segments: {segments}")
        # 4. subsegment
        return_data = []
        selected_segments = []
        for item in segments:
            begin, end = item["start"], item["end"]
            if end - begin >= min_duration:
                begin_idx = int(begin * sample_rate)
                end_idx = int(end * sample_rate)
                return_data.append(pcm[:, begin_idx:end_idx])  # [c, time]
                selected_segments.append(item)
            else:
                self.echo(f"Skip segment: {item}")
        # 5. return
        # [n, c, time] -> [c, n*time]
        if len(return_data) == 0:
            remove_file(tmp_audio_path)
            return {
                "pcm": None,
                "sample_rate": sample_rate,
                "segments": selected_segments,
            }
        return_data = torch.cat(return_data, dim=-1)
        self.echo(
            f"After VAD: {return_data.shape}, sample_rate: {sample_rate}, length: {return_data.shape[1]/sample_rate:.2f}"
        )
        self.echo(f"Useful radio: {return_data.shape[1]*100/pcm.shape[1]:.2f}%")
        # save to {DGUARD_MODEL_PATH}/tmp/{filename}.wav
        if self.save_vad_path:
            filename = os.path.basename(audio_path).split(".")[0]
            os.makedirs(self.save_vad_path, exist_ok=True)
            torchaudio.save(
                f"{self.save_vad_path}/{filename}.wav", return_data, sample_rate
            )
        # rm tmp_audio_path if exist
        if tmp_audio_path:
            remove_file(tmp_audio_path)
        result = {
            "pcm": return_data,
            "sample_rate": sample_rate,
            "segments": selected_segments,
        }
        return result

    def vad_list(self, audio_paths, use_energy_vad=False):
        result = []
        for audio_path in audio_paths:
            result.append(self.vad_file(audio_path, use_energy_vad=use_energy_vad))
        return result

    def extract_embedding_feats(self, fbanks, batch_size, subseg_cmn):
        fbanks_array = np.stack(fbanks)
        if subseg_cmn:
            fbanks_array = fbanks_array - np.mean(fbanks_array, axis=1, keepdims=True)
        embeddings = []
        fbanks_array = torch.from_numpy(fbanks_array).to(self.device)
        # for i in tqdm(range(0, fbanks_array.shape[0], batch_size)):  # tqdm()
        for i in range(0, fbanks_array.shape[0], batch_size):  # tqdm()
            batch_feats = fbanks_array[i : i + batch_size]
            batch_embs = self.embedding_models[0](batch_feats)
            batch_embs = batch_embs[-1] if isinstance(batch_embs, tuple) else batch_embs
            embeddings.append(batch_embs.detach().cpu().numpy())
        embeddings = np.vstack(embeddings)
        return embeddings

    def diarize(self, audio_path: str, utt: str = "dguard", save_audio_folder=None, use_energy_vad=False):
        # tmp_audio_path = (
        #     audio_path.filename + f"_channel_{self.channel}.wav"
        #     if hasattr(audio_path, "filename")
        #     else audio_path + f"_channel_{self.channel}.wav"
        # )

        audio_save_name = os.path.basename(audio_path).split(".")[0]
        now_uuid = str(uuid.uuid1())
        # assert {DGUARD_MODEL_PATH}/tmp exists, if not, create it
        if not os.path.exists(f"{DGUARD_MODEL_PATH}/tmp"):
            os.makedirs(f"{DGUARD_MODEL_PATH}/tmp", exist_ok=True)
        tmp_audio_path = f"{DGUARD_MODEL_PATH}/tmp/{audio_save_name}_{now_uuid}_channel{self.channel}.wav"

        pcm, sample_rate = load_wav(
            audio_path,
            sr=self.sample_rate,
            channel=self.channel,
            wavform_normalize=False,
            saveto=tmp_audio_path,
            start_time=self.start_time,
        )

        # 1. vad
        # vad_segments = self.vad.get_speech_timestamps(
        #     tmp_audio_path, return_seconds=True, use_energy_vad=use_energy_vad
        # )
        if use_energy_vad:
            vad_segments = self.vad.get_speech_timestamps_energy(
                data=pcm, sample_rate=sample_rate, return_seconds=True
            )
        else:
            vad_segments = self.vad.get_speech_timestamps(
                data=pcm, sample_rate=sample_rate, return_seconds=True
            )

        # 2. extact fbanks
        subsegs, subseg_fbanks = [], []
        window_fs = int(self.diar_window_secs * 1000) // self.diar_frame_shift
        period_fs = int(self.diar_period_secs * 1000) // self.diar_frame_shift
        split_num = 0
        for _, item in enumerate(vad_segments):
            try:
                begin, end = item["start"], item["end"]
                if end - begin >= self.diar_min_duration:
                    begin_idx = int(begin * sample_rate)
                    end_idx = int(end * sample_rate)
                    tmp_wavform = pcm[0, begin_idx:end_idx].unsqueeze(0).to(torch.float)
                    fbank = self.feature_extractor(tmp_wavform)
                    tmp_subsegs, tmp_subseg_fbanks = subsegment(
                        fbank=fbank,
                        seg_id="{:08d}-{:08d}".format(
                            int(begin * 1000), int(end * 1000)
                        ),
                        window_fs=window_fs,
                        period_fs=period_fs,
                        frame_shift=self.diar_frame_shift,
                    )
                    subsegs.extend(tmp_subsegs)
                    subseg_fbanks.extend(tmp_subseg_fbanks)
                    split_num += 1
                    if split_num >= self.diar_max_split_num:
                        break
            except Exception as e:
                logger.error(f"Error: {e}")
                logger.error(f"Skip segment: {item}")
                continue

        # 3. extract embedding
        embeddings = self.extract_embedding_feats(
            subseg_fbanks, self.diar_batch_size, self.diar_subseg_cmn
        )

        # 4. cluster
        subseg2label = []
        labels = cluster(
            embeddings,
            num_spks=self.diar_num_spks,
            min_num_spks=self.diar_min_num_spks,
            max_num_spks=self.diar_max_num_spks,
        )
        for _subseg, _label in zip(subsegs, labels):
            # b, e = process_seg_id(_subseg, frame_shift=self.diar_frame_shift)
            # subseg2label.append([b, e, _label])
            begin_ms, end_ms, begin_frames, end_frames = _subseg.split("-")
            begin = (int(begin_ms) + int(begin_frames) * self.diar_frame_shift) / 1000.0
            end = (int(begin_ms) + int(end_frames) * self.diar_frame_shift) / 1000.0
            subseg2label.append([begin, end, _label])

        # 5. merged segments
        # [[utt, ([begin, end, label], [])], [utt, ([], [])]]
        merged_segment_to_labels = merge_segments({utt: subseg2label})
        if save_audio_folder:
            if not os.path.exists(save_audio_folder):
                os.makedirs(save_audio_folder, exist_ok=True)
            all_data = {}
            for i, (utt, begin, end, label) in enumerate(merged_segment_to_labels):
                if label not in all_data:
                    all_data[label] = {}
                    all_data[label]["pcm"] = []
                    all_data[label]["length"] = 0

                begin_idx = int(begin * sample_rate)
                end_idx = int(end * sample_rate)
                all_data[label]["pcm"].append(pcm[0, begin_idx:end_idx].unsqueeze(0))
                all_data[label]["length"] += end_idx - begin_idx
            # sort by length
            _label = all_data.keys()
            lengths = [[label, all_data[label]["length"]] for label in _label]
            lengths = sorted(lengths, key=lambda x: x[1], reverse=True)
            for i, data in enumerate(lengths):
                label = data[0]
                dict_data = all_data[label]
                pcm_data = torch.cat(dict_data["pcm"], dim=-1)
                torchaudio.save(f"{save_audio_folder}/{i+1}.wav", pcm_data, sample_rate)
        remove_file(tmp_audio_path)
        return merged_segment_to_labels

    def make_rttm(self, merged_segment_to_labels, outfile):
        with open(outfile, "w", encoding="utf-8") as fin:
            for utt, begin, end, label in merged_segment_to_labels:
                fin.write(
                    "SPEAKER {} {} {:.3f} {:.3f} <NA> <NA> {} <NA> <NA>\n".format(
                        utt, 1, float(begin), float(end) - float(begin), label
                    )
                )

    def quality(self, wav_file=None, channel=None, detail=False, use_vad=True, data=None, sr=None):
        if data is not None and sr is not None:
            if len(data.shape) != 1 and data.shape[0] != 1:
                data = data[self.channel, :]
            wav_data = data
            if use_vad:
                r = self.vad_file(
                    data=data, sr=sr, use_energy_vad=True
                )
                wav_data, sr, _ = r["pcm"], r["sample_rate"], r["segments"]
        else:
            if use_vad:
                r = self.vad_file(
                    wav_file, channel, use_energy_vad=True
                )
                wav_data, sr, _ = r["pcm"], r["sample_rate"], r["segments"]
            else:
                wav_data, sr = load_wav(
                    wav_file,
                    sr=self.sample_rate,
                    channel=self.channel if channel is None else channel,
                    wavform_normalize=self.wavform_normalize,
                    start_time=self.start_time,
                )
        
        if sr != self.sample_rate:
            self.echo(f"Warning: {wav_file} sample rate is {sr}, not {self.sample_rate}")
            raise ValueError(f"Sample rate {sr} is not supported, please use {self.sample_rate}")
        wav_data = wav_data.reshape(1, -1)
        first, second = wav_data[:, : wav_data.shape[1] // 2], wav_data[:, wav_data.shape[1] // 2 :]
        if first.shape[1] < sr * 3:
            first = torch.cat([first, torch.zeros((1, sr * 3 - first.shape[1]))], dim=1)
        else:
            first = first[:, :sr * 3]
        if second.shape[1] < sr * 3:
            second = torch.cat([torch.zeros((1, sr * 3 - second.shape[1])), second], dim=1)
        else:
            second = second[:, -sr * 3:]
        first_feature = self.feature_extractors[0](first)
        second_feature = self.feature_extractors[0](second)
        first_emb = self.embedding_models[0](first_feature.unsqueeze(0).to(self.device))
        first_emb = first_emb[-1] if isinstance(first_emb, tuple) else first_emb
        second_emb = self.embedding_models[0](second_feature.unsqueeze(0).to(self.device))
        second_emb = second_emb[-1] if isinstance(second_emb, tuple) else second_emb
        first_emb = first_emb / torch.norm(first_emb, p=2)
        second_emb = second_emb / torch.norm(second_emb, p=2)
        similarity = torch.dot(first_emb.reshape(-1), second_emb.reshape(-1))
        similarity = similarity.item()
        similarity = (similarity+1)/2.0
        similarity = similarity * 10
        return {
            "P808_MOS": similarity
        }

    @staticmethod
    def info():
        all_models_len = len(ALL_MODELS)
        print(f"Total {all_models_len} models found in Dguard.")
        _index = 1
        print(f"{'#':<5} {'Model Name':<50} {'EmSiz':<5} {'SR':<5} {'Time':<20}")
        for k, v in MI.items():
            model_name = k
            model_info = v
            embedding_size = model_info.get("embedding_size", "None")
            sample_rate = model_info.get("sample_rate", "None")
            update_time = model_info.get("add_time", "None")
            print(
                f"{_index:<5} {model_name:<50} {embedding_size:<5} {sample_rate:<5} {update_time:<20}"
            )
            _index += 1
