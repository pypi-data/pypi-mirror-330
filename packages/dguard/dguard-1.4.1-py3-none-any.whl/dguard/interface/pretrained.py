# coding = utf-8
# @Time    : 2023-08-02  09:00:45
# @Author  : zhaosheng@nuaa.edu.cn
# @Describe: Load pretrained model by name.

import os
import torch.nn.functional as F
import wget
import asyncio
import websockets
import soundfile as sf

# Models
from dguard.interface.models_info import model_info
from dguard.interface.model_wrapper import load_model

# Logger
from dguard.utils import logger

ALL_MODELS = list(model_info.keys())

# Load DGUARD_MODEL_PATH from environment variable, if not found, use default path
DGUARD_MODEL_PATH = os.getenv("DGUARD_MODEL_PATH", "/tmp/dguard")
os.makedirs(DGUARD_MODEL_PATH, exist_ok=True)
# logger.info(f"* Using Default Model Path: {DGUARD_MODEL_PATH}")


def download_or_load(url):
    # Download the model
    if url.startswith("http"):
        ckpt_path = f"{DGUARD_MODEL_PATH}/{os.path.basename(url)}"
        if os.path.exists(ckpt_path):
            return ckpt_path
        else:
            logger.info(
                f"Model not found, downloading from {url} -> {DGUARD_MODEL_PATH}"
            )
        wget.download(url, out=DGUARD_MODEL_PATH)
    else:
        ckpt_path = url
    if not os.path.exists(ckpt_path):
        raise FileNotFoundError(
            f"Model file {ckpt_path} not found and it is not a valid URL."
        )
    return ckpt_path


def load_by_name(
    model_name,
    device="cuda:0",
    strict=True,
    loader="wespeaker",
    feature_extractor=True,
):
    if model_name in model_info:
        pt_path = model_info[model_name].get("pt", None)
        loader = model_info[model_name].get("loader", loader)
        if not pt_path:
            pt_path = f"{DGUARD_MODEL_PATH}/{model_name}.pt"
        pt_path = download_or_load(pt_path)
        yaml_path = model_info[model_name].get("yaml", None)
        if not yaml_path:
            yaml_path = f"{DGUARD_MODEL_PATH}/{model_name}.yaml"
        yaml_path = download_or_load(yaml_path)
        embedding_size = int(model_info[model_name]["embedding_size"])
        sample_rate = int(model_info[model_name]["sample_rate"])
        feat_dim = int(model_info[model_name].get("feat_dim", 80))
        dguard_model = load_model(
            loader,
            pt_path,
            yaml_path,
            strict,
            device,
            embedding_size,
            sample_rate,
            feat_dim,
            feature_extractor,
        )
        return dguard_model
    else:
        logger.error(f"Model {model_name} not found in model_info.")
        logger.info("\t*-> All models: ", ALL_MODELS)
        raise NotImplementedError(f"Model {model_name} not implemented.")


class PretrainedModel:
    def __init__(
        self, model_name, device="cpu", strict=True, loader="wespeaker"
    ):
        self.model = load_by_name(
            model_name=model_name, device=device, strict=strict, loader=loader
        )
        self.model.wavform_normalize = model_info[model_name].get(
            "wavform_normalize", False
        )
        logger.info(f"   *-> Load model {model_name} successfully.")

    def interface(self, wav_path_list, length=-1, start_time=0, mean=False):
        return self.model.encode_list(
            wav_files=wav_path_list,
            length=length,
            start_time=start_time,
            mean=mean,
        )

    def calculate_cosine_distance(self, x, y):
        x = x.reshape(1, -1)
        y = y.reshape(1, -1)
        cos_sim = F.cosine_similarity(x, y, dim=-1)
        return cos_sim

    def print_help(self):
        print(f"Model Name: {self.model_name}")
        print(f"Embedding Size: {self.model.embedding_size}")
        print(f"Sample Rate: {self.model.sample_rate}")
        print(f"Waveform Normalize: {self.model.wavform_normalize}")
        print(f"Usage: ")
        print(
            f"  1. Call 'calculate_cosine_distance' to calculate cosine similarity between two embeddings."
        )
        print(
            f"     e.g. similarity = model.calculate_cosine_distance(embeddings[0],embeddings[1])"
        )
        print(
            f"  2. Call 'inference' to get the inference result of a list of wav files."
        )
        print(
            f"     e.g. result = model.inference(wav_path_list=['a.wav','b.wav'])"
        )


class WebSocketClient:
    def __init__(self, length=10, start=0, model_name=None):
        self.length = length
        self.start = start
        self.model_name = model_name

    async def test_websocket_server(self, wav_path, WEBSOCKET_URI):
        async with websockets.connect(WEBSOCKET_URI) as websocket:
            audio_data, sample_rate = sf.read(wav_path, dtype="int16")
            # audio data read from start(s) to start(s)+length(s)
            logger.info(
                f"Audio data shape: {audio_data.shape}, sample rate: {sample_rate}"
            )
            audio_data = audio_data[
                int(self.start * sample_rate) : int(
                    (self.start + self.length) * sample_rate
                )
            ]
            logger.info(f"Cropped audio data shape: {audio_data.shape}")
            await websocket.send(audio_data.tobytes())
            response = await websocket.recv()
            response = response.strip()
            response = [float(x) for x in response.split(" ")]
            logger.info("Received response from server:", response)
            return response

    def inference(self, wav_path_list, print_info=False):
        logger.info(f"* Model name: {self.model_name}")
        WEBSOCKET_URI = f"ws://localhost:9799"
        result = []
        for wav_path in wav_path_list:
            output = asyncio.get_event_loop().run_until_complete(
                self.test_websocket_server(wav_path, WEBSOCKET_URI)
            )
            result.append([output, 0, 0, 0, 0])
        return result
