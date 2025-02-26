import os

from dguard.asr.aliasr.auto.auto_model import AutoModel
from dguard.asr.aliasr.utils.postprocess_utils import rich_transcription_postprocess


class DguardASR:
    def __init__(self, apply_vad=False, device="cuda:0"):
        DGUARD_MODEL_PATH = os.getenv("DGUARD_MODEL_PATH", None)
        if DGUARD_MODEL_PATH is not None:
            model_dir = os.path.join(DGUARD_MODEL_PATH, "aliasr")
            vad_dir = os.path.join(DGUARD_MODEL_PATH, "aliasr", "vad")
        else:
            # use ~/.dguard as default
            print(f"DGUARD_MODEL_PATH is not set, using default path: {DGUARD_MODEL_PATH}")
            DGUARD_MODEL_PATH = os.path.expanduser("~/.dguard")
            model_dir = os.path.join(DGUARD_MODEL_PATH, "aliasr")
            vad_dir = os.path.join(DGUARD_MODEL_PATH, "aliasr", "vad")
            if not os.path.exists(DGUARD_MODEL_PATH):
                raise FileNotFoundError(
                    f"DGUARD_MODEL_PATH is not set, and default path {DGUARD_MODEL_PATH} does not exist."
                )
            if not os.path.exists(model_dir):
                raise FileNotFoundError(
                    f"Model file {model_dir} does not exist in default path {DGUARD_MODEL_PATH}."
                )
            if not os.path.exists(vad_dir):
                raise FileNotFoundError(
                    f"Model file {vad_dir} does not exist in default path {DGUARD_MODEL_PATH}."
                )
            
        if apply_vad and os.path.exists(vad_dir):
            vad_model = "vad"
            vad_model_dir = vad_dir
            vad_kwargs = {"max_single_segment_time": 30000}
        else:
            vad_model = None
            vad_model_dir = None
            vad_kwargs = None

        self.model = AutoModel(
            model=model_dir,
            vad_model=vad_model,
            vad_model_dir=vad_model_dir,
            vad_kwargs=vad_kwargs,
            device=device,
        )

    def infer(self, audio_path, language="zh"):
        res = self.model.generate(
            input=audio_path,
            cache={},
            language=language,  # "zn", "en", "yue", "ja", "ko", "nospeech"
            use_itn=True,
            batch_size_s=60,
            merge_vad=True,  #
            merge_length_s=15,
        )
        text = rich_transcription_postprocess(res[0]["text"])
        return text


if __name__ == "__main__":
    asr = DguardASR(device="cpu")
    audio_path = (
        "/home/zhaosheng/Documents/dguard_project/dguard_home/aliasr/example/zh.mp3"
    )
    text = asr.infer(audio_path)
    print(text)
