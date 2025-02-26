# coding = utf-8
# @Time    : 2024-05-21  09:02:30
# @Author  : zhaosheng@lyxxkj.com.cn
# @Describe: Dguard Client.

import asyncio
import base64
import getpass
import os
import subprocess

import numpy as np
import torch
import torchaudio
import websockets
import yaml
from cryptography.fernet import Fernet
from tqdm import tqdm

from dguard.interface.models_info import model_info as MI
from dguard.process.processor import FBank_kaldi
from dguard.speaker.diar.extract_emb import subsegment
from dguard.speaker.diar.make_rttm import merge_segments
from dguard.speaker.diar.spectral_clusterer import cluster
from dguard.speaker.models.speaker_model import get_speaker_model
from dguard.speaker.utils.utils import set_seed
from dguard.utils import logger

# Utils
from dguard.utils.builder import build
from dguard.utils.config import yaml_config_loader
from dguard.utils.dguard_model_utils import (
    ALL_MODELS,
    DGUARD_MODEL_PATH,
    download_or_load,
    load_model_tiny_model,
    load_wav,
    remove_file,
)
from dguard.utils.wespeaker_checkpoint import load_checkpoint
from dguard.vad.dguard_vad import VAD


class WebSocketClient:
    def __init__(
        self,
        ws_servers,
        embedding_sizes,
        embedding_model_names,
        wavform_normalize=False,
        sample_rate=16000,
        channel=0,
        length=10,
        start_time=0,
        verbose=False,
        max_split_num=5,
        mean=False,
        apply_vad=False,
        vad_min_duration=0.25,
        vad_smooth_threshold=0.25,
        save_vad_path=None,
        seed=42,
    ):
        set_seed(seed)
        self.ws_servers = ws_servers
        self.channel = channel
        self.length = length
        self.start_time = start_time
        self.max_split_num = max_split_num
        self.mean = mean
        self.embedding_sizes = embedding_sizes
        self.wavform_normalize = wavform_normalize
        self.sample_rate = sample_rate
        self.apply_vad = apply_vad
        if apply_vad:
            self.vad = VAD()
        self.min_duration = vad_min_duration
        self.smooth_threshold = vad_smooth_threshold
        self.save_vad_path = save_vad_path
        self.verbose = verbose
        self.embedding_model_names = embedding_model_names

    async def test_websocket_server(self, audio_data, ws_server):
        audio_data = audio_data.reshape(1, -1)
        audio_data = np.array(audio_data).astype(np.int16)
        async with websockets.connect(ws_server) as websocket:
            await websocket.send(audio_data.tobytes())
            response = await websocket.recv()
            response = response.strip()
            response = [float(x) for x in response.split(" ")]
            response = torch.from_numpy(np.array(response))
            return response

    def vad_file(self, audio_path):
        min_duration = self.min_duration
        smooth_threshold = self.smooth_threshold
        pcm, sample_rate = load_wav(
            audio_path,
            sr=self.sample_rate,
            channel=self.channel,
            wavform_normalize=False,
        )
        self.echo(
            f"Before VAD: {pcm.shape}, sample_rate: {sample_rate}, length: {pcm.shape[1]/sample_rate:.2f}"
        )
        # 1. vad
        try:
            vad_segments = self.vad.get_speech_timestamps(
                audio_path, return_seconds=True
            )
        except Exception as e:
            logger.error(f"VAD failed: {e}")
            vad_segments = []
            return {
                "pcm": None,
                "sample_rate": sample_rate,
                "segments": vad_segments,
            }
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
        return_data = torch.cat(return_data, dim=-1)
        self.echo(
            f"After VAD: {return_data.shape}, sample_rate: \{sample_rate}, length: {return_data.shape[1]/sample_rate:.2f}"
        )
        self.echo(f"Useful radio: {return_data.shape[1]*100/pcm.shape[1]:.2f}%")
        # save to {DGUARD_MODEL_PATH}/tmp/{filename}.wav
        if self.save_vad_path:
            filename = os.path.basename(audio_path).split(".")[0]
            os.makedirs(self.save_vad_path, exist_ok=True)
            torchaudio.save(
                f"{self.save_vad_path}/{filename}.wav", return_data, sample_rate
            )
        result = {
            "pcm": return_data,
            "sample_rate": sample_rate,
            "segments": selected_segments,
        }
        return result

    def echo(self, text):
        if self.verbose:
            logger.info(text)

    def encode(self, wav_file):
        length = self.length
        start_time = self.start_time
        mean = self.mean
        if self.apply_vad:
            self.echo(f"Load {wav_file} with VAD")
            r = self.vad_file(wav_file)
            wav_data, sr, _ = r["pcm"], r["sample_rate"], r["segments"]
        else:
            self.echo(f"Load {wav_file} without VAD")
            wav_data, sr = load_wav(
                wav_file,
                sr=self.sample_rate,
                channel=self.channel,
                wavform_normalize=False,
            )
        wav_data = wav_data.to(torch.float32)
        if sr != self.sample_rate:
            logger.warning(f"Resampling {wav_file} from {sr} to {self.sample_rate}")
            wav_data = torchaudio.transforms.Resample(
                orig_freq=sr, new_freq=self.sample_rate
            )(wav_data)
        sr = self.sample_rate
        raw_length = wav_data.shape[1] / sr  # seconds
        raw_length = raw_length - start_time  # seconds
        if raw_length < 0:
            # raise error
            logger.error(f"Start time {start_time} is larger than length of {wav_file}")
            raise ValueError(
                f"Start time {start_time} is larger than length of {wav_file}"
            )
        if raw_length < length:
            length = raw_length
        start = start_time * sr  # samples
        if length < 0:
            split_num = 1
            tiny_length = raw_length
        else:
            split_num = int(raw_length / length)
            tiny_length = length * sr  # samples
        self.echo(
            f"Split {wav_file} into {split_num} parts, RAW length(samples): {raw_length*sr}, TINY length(samples): {tiny_length}"
        )

        _tmp_embs = []
        for split_index in range(split_num):
            if split_index == self.max_split_num:
                break
            if split_index == split_num - 1:
                now_start = int(start + split_index * tiny_length)
                wav_data_now = wav_data.clone()[:, now_start:]
            else:
                now_start = int(start + split_index * tiny_length)
                now_end = int(start + (split_index + 1) * tiny_length)
                wav_data_now = wav_data.clone()[:, now_start:now_end]
            # wav_data_now -> torch.int16
            # wav_data_now = wav_data_now.to(torch.int16)
            if not mean:
                emb = self.get_embedding_from_ws(wav_data_now)
                self.echo(f"  # Get emb from 1st split, shape: {emb.shape}")
                self.echo(f"  # Tiny length: {tiny_length}")
                return emb
            else:  # Mean of all splits
                emb = self.get_embedding_from_ws(wav_data_now)
                _tmp_embs.append(emb)
        mean_emb = torch.stack(_tmp_embs).mean(0)
        self.echo(f"mean_emb shape: {mean_emb.shape}")
        self.echo(
            f"  # Get mean emb from {min(self.max_split_num,split_num)} splits, shape: {mean_emb.shape}"
        )
        self.echo(f"  # Tiny length: {tiny_length}")
        return mean_emb

    def encode_list(self, wav_files):
        result = []
        for wav in wav_files:
            result.append(self.encode(wav))
        return result

    def cosine_similarity(self, e1, e2):
        e1 = e1.to(torch.float32)
        e2 = e2.to(torch.float32)
        assert e1.shape == e2.shape
        all_scores = []
        result = {"scores": {}}
        start = 0
        for _index, embedding_size in enumerate(self.embedding_sizes):
            e1_now = e1[start : start + embedding_size]
            e2_now = e2[start : start + embedding_size]
            start += embedding_size
            cosine_score = torch.dot(e1_now, e2_now) / (
                torch.norm(e1_now) * torch.norm(e2_now)
            )
            cosine_score = cosine_score.item()
            self.echo(
                f"    -> Model {self.embedding_model_names[_index]}: {cosine_score}"
            )
            all_scores.append(cosine_score)
            result["scores"][self.embedding_model_names[_index]] = cosine_score
        mean_scores = sum(all_scores) / len(all_scores)
        # return mean_scores
        result["mean_score"] = mean_scores
        return result

    def cosine_similarity_list(self, embeddings1, embeddings2):
        assert len(embeddings1) == len(embeddings2)
        result = []
        for e1, e2 in zip(embeddings1, embeddings2):
            result.append(self.cosine_similarity(e1, e2))
        return result

    def file_similarity(self, wav1, wav2, id1=None, id2=None):
        if id1 is not None:
            if id1 in self.table:
                e1 = self.table[id1]
            else:
                e1 = self.encode(wav1)
                self.table[id1] = e1
        else:
            e1 = self.encode(wav1)

        if id2 is not None:
            if id2 in self.table:
                e2 = self.table[id2]
            else:
                e2 = self.encode(wav2)
                self.table[id2] = e2
        else:
            e2 = self.encode(wav2)
        return self.cosine_similarity(e1, e2)

    def file_similarity_list(self, trial_list):
        result = []
        # trial: (wav1, wav2, id1, id2)
        for trial in trial_list:
            if len(trial) == 2:
                trial.append(None)
                trial.append(None)
            assert (
                len(trial) == 4
            ), f"Trial {trial} is not valid, Please check the format, Make sure it is [wav1, wav2, id1, id2]"
            result.append(self.file_similarity(trial[0], trial[1], trial[2], trial[3]))
        return result

    def vad_list(self, audio_paths):
        result = []
        for audio_path in audio_paths:
            result.append(self.vad_file(audio_path))
        return result

    def get_embedding_from_ws(self, wav_data):
        # to int 16
        wav_data = wav_data.to(torch.int16)
        _tmp_embs = []
        for _index, ws_server in enumerate(self.ws_servers):
            emb = asyncio.get_event_loop().run_until_complete(
                self.test_websocket_server(wav_data, ws_server)
            )
            emb = emb.reshape(-1)
            _tmp_embs.append(emb)
        result = torch.cat(_tmp_embs, dim=0)
        return result
