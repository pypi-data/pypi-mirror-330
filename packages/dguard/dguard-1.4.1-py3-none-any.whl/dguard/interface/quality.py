# coding = utf-8
# @Time    : 2024-12-16  17:26:28
# @Author  : zhaosheng@lyxxkj.com.cn
# @Describe: Mos model.

import os
import uuid
import librosa
import numpy as np
import onnxruntime as ort
import soundfile as sf

from dguard.utils.dguard_model_utils import DGUARD_MODEL_PATH
from dguard.utils.dguard_model_utils import download_or_load, load_wav, remove_file

SAMPLING_RATE = 16000
INPUT_LENGTH = 9.01


class ComputeScore:
    def __init__(self, primary_model_path, p808_model_path) -> None:
        self.onnx_sess = ort.InferenceSession(primary_model_path, providers=['CUDAExecutionProvider']) # , 'CPUExecutionProvider'
        self.p808_onnx_sess = ort.InferenceSession(p808_model_path, providers=['CUDAExecutionProvider']) # , 'CPUExecutionProvider'

    def audio_melspec(
        self, audio, n_mels=120, frame_size=320, hop_length=160, sr=16000, to_db=True
    ):
        mel_spec = librosa.feature.melspectrogram(
            y=audio, sr=sr, n_fft=frame_size + 1, hop_length=hop_length, n_mels=n_mels
        )
        if to_db:
            mel_spec = (librosa.power_to_db(mel_spec, ref=np.max) + 40) / 40
        return mel_spec.T

    def get_polyfit_val(self, sig, bak, ovr, is_personalized_MOS):
        if is_personalized_MOS:
            p_ovr = np.poly1d([-0.00533021, 0.005101, 1.18058466, -0.11236046])
            p_sig = np.poly1d([-0.01019296, 0.02751166, 1.19576786, -0.24348726])
            p_bak = np.poly1d([-0.04976499, 0.44276479, -0.1644611, 0.96883132])
        else:
            p_ovr = np.poly1d([-0.06766283, 1.11546468, 0.04602535])
            p_sig = np.poly1d([-0.08397278, 1.22083953, 0.0052439])
            p_bak = np.poly1d([-0.13166888, 1.60915514, -0.39604546])

        sig_poly = p_sig(sig)
        bak_poly = p_bak(bak)
        ovr_poly = p_ovr(ovr)

        return sig_poly, bak_poly, ovr_poly

    def __call__(self, fpath, sampling_rate, is_personalized_MOS):
        aud, input_fs = sf.read(fpath)
        fs = sampling_rate
        if input_fs != fs:
            audio = librosa.resample(aud, input_fs, fs)
        else:
            audio = aud
        actual_audio_len = len(audio)
        len_samples = int(INPUT_LENGTH * fs)
        while len(audio) < len_samples:
            audio = np.append(audio, audio)

        num_hops = int(np.floor(len(audio) / fs) - INPUT_LENGTH) + 1
        hop_len_samples = fs
        predicted_mos_sig_seg_raw = []
        predicted_mos_bak_seg_raw = []
        predicted_mos_ovr_seg_raw = []
        predicted_mos_sig_seg = []
        predicted_mos_bak_seg = []
        predicted_mos_ovr_seg = []
        predicted_p808_mos = []
        num_hops = min(1, num_hops) # Only one hop
        for idx in range(num_hops):
            audio_seg = audio[
                int(idx * hop_len_samples) : int((idx + INPUT_LENGTH) * hop_len_samples)
            ]
            if len(audio_seg) < len_samples:
                continue

            input_features = np.array(audio_seg).astype("float32")[np.newaxis, :]
            p808_input_features = np.array(
                self.audio_melspec(audio=audio_seg[:-160])
            ).astype("float32")[np.newaxis, :, :]
            oi = {"input_1": input_features}
            p808_oi = {"input_1": p808_input_features}
            p808_mos = self.p808_onnx_sess.run(None, p808_oi)[0][0][0]
            mos_sig_raw, mos_bak_raw, mos_ovr_raw = self.onnx_sess.run(None, oi)[0][0]
            mos_sig, mos_bak, mos_ovr = self.get_polyfit_val(
                mos_sig_raw, mos_bak_raw, mos_ovr_raw, is_personalized_MOS
            )
            predicted_mos_sig_seg_raw.append(mos_sig_raw)
            predicted_mos_bak_seg_raw.append(mos_bak_raw)
            predicted_mos_ovr_seg_raw.append(mos_ovr_raw)
            predicted_mos_sig_seg.append(mos_sig)
            predicted_mos_bak_seg.append(mos_bak)
            predicted_mos_ovr_seg.append(mos_ovr)
            predicted_p808_mos.append(p808_mos)

        clip_dict = {"filename": fpath, "len_in_sec": actual_audio_len / fs, "sr": fs}
        clip_dict["num_hops"] = num_hops
        clip_dict["OVRL_raw"] = np.mean(predicted_mos_ovr_seg_raw)
        clip_dict["SIG_raw"] = np.mean(predicted_mos_sig_seg_raw)
        clip_dict["BAK_raw"] = np.mean(predicted_mos_bak_seg_raw)
        clip_dict["OVRL"] = np.mean(predicted_mos_ovr_seg)
        clip_dict["SIG"] = np.mean(predicted_mos_sig_seg)
        clip_dict["BAK"] = np.mean(predicted_mos_bak_seg)
        clip_dict["P808_MOS"] = np.mean(predicted_p808_mos)
        return clip_dict

class DguardMos:
    def __init__(self, personalized_MOS=False, channel=0, start_time=0):
        self.personalized_MOS = personalized_MOS
        p808_model_path = download_or_load(
            f"https://www.modelscope.cn/api/v1/models/nuaazs/vaf/repo?Revision=master&FilePath=model_v8.onnx"
        )
        if personalized_MOS:
            primary_model_path = download_or_load(
                f"https://www.modelscope.cn/api/v1/models/nuaazs/vaf/repo?Revision=master&FilePath=p_sig_bak_ovr.onnx"
            )
        else:
            primary_model_path = download_or_load(
                f"https://www.modelscope.cn/api/v1/models/nuaazs/vaf/repo?Revision=master&FilePath=sig_bak_ovr.onnx"
            )
        self.compute_score = ComputeScore(primary_model_path, p808_model_path)
        self.is_personalized_eval = personalized_MOS
        self.desired_fs = 16000
        self.channel = channel
        self.start_time = start_time

    def dnsmos(self, audio_path):

        audio_save_name = os.path.basename(audio_path).split(".")[0]
        now_uuid = str(uuid.uuid1())
        # assert {DGUARD_MODEL_PATH}/tmp exists, if not, create it
        if not os.path.exists(f"{DGUARD_MODEL_PATH}/tmp"):
            os.makedirs(f"{DGUARD_MODEL_PATH}/tmp", exist_ok=True)
        tmp_audio_path = f"{DGUARD_MODEL_PATH}/tmp/{audio_save_name}_{now_uuid}_channel{self.channel}.wav"

        pcm, sample_rate = load_wav(
            audio_path,
            sr=16000,
            channel=self.channel,
            wavform_normalize=False,
            saveto=tmp_audio_path,
            start_time=self.start_time,
        )

        result = self.compute_score(
            tmp_audio_path, self.desired_fs, self.is_personalized_eval
        )
        remove_file(tmp_audio_path)
        return result

if __name__ == "__main__":
    mos = DguardMos()
    for _ in range(10):
        result = mos.dnsmos(
            "/home/zhaosheng/Documents/dguard_project/test/data/test.wav"
        )
        print(result)