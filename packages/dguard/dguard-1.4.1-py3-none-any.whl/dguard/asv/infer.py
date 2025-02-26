# coding = utf-8
# @Time    : 2024-12-17  19:13:45
# @Author  : zhaosheng@lyxxkj.com.cn
# @Describe: ASV model.

import os
from dguard.asv.asv import load_trained_model, DEFAULT_CONFIG, predict_single_audio

class DguardASV:
    def __init__(self, device="cuda:0", threshold=0):
        DGUARD_MODEL_PATH = os.getenv("DGUARD_MODEL_PATH", None)
        if DGUARD_MODEL_PATH is not None:
            model_path = os.path.join(DGUARD_MODEL_PATH, "dguard_asv_20250210.pt")
        else:
            # use ~/.dguard as default
            print(f"DGUARD_MODEL_PATH is not set, using default path: {DGUARD_MODEL_PATH}")
            DGUARD_MODEL_PATH = os.path.expanduser("~/.dguard")
            model_path = os.path.join(DGUARD_MODEL_PATH, "dguard_asv_20250210.pt")
            if not os.path.exists(DGUARD_MODEL_PATH):
                raise FileNotFoundError(
                    f"DGUARD_MODEL_PATH is not set, and default path {DGUARD_MODEL_PATH} does not exist."
                )
            if not os.path.exists(model_path):
                raise FileNotFoundError(
                    f"Model file {model_path} does not exist in default path {DGUARD_MODEL_PATH}."
                )
        self.device = device
        self.configs = DEFAULT_CONFIG
        self.model = load_trained_model(self.configs, model_path, self.device)

    def infer(self, audio_path, channel=0, length=-1):
        result = predict_single_audio(audio_path, self.model, self.configs, self.device)
        print(result)
        return {
            "score": result["confidence"] if result["prediction"] == 1 else 1 - result["confidence"],
            "label": "Fake" if result["prediction"] == 1 else "Real",
        }


if __name__ == "__main__":
    asv = DguardASV(device="cuda")
    audio_path = (
        "/home/xingxuyang/project/train_16k/zhaohang/ADD2023_GEN/000003_SSB0737.wav"
    )
    DF_result = asv.infer(audio_path)
    print(DF_result)
