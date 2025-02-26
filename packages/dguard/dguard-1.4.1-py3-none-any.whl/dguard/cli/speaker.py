# coding = utf-8
# @Time    : 2024-12-16  16:50:26
# @Author  : zhaosheng@lyxxkj.com.cn
# @Describe: Speaker Class.

import sys

import kaldiio
import numpy as np
import torch
import torchaudio
from tqdm import tqdm

from dguard.cli.utils import get_args
from dguard.interface.pretrained import load_by_name
from dguard.speaker.diar.extract_emb import subsegment
from dguard.speaker.diar.make_rttm import merge_segments
from dguard.speaker.diar.spectral_clusterer import cluster
from dguard.speaker.utils.utils import set_seed
from dguard.vad.dguard_vad import VAD


class Speaker:
    def __init__(
        self,
        model_name,
        device="cpu",
        loader="wespeaker",
        apply_vad=False,
        diar_num_spks=None,
        diar_min_num_spks=1,
        diar_max_num_spks=20,
        diar_min_duration=0.255,
        diar_window_secs=1.5,
        diar_period_secs=0.75,
        diar_frame_shift=10,
        diar_batch_size=32,
        diar_subseg_cmn=True,
    ):
        set_seed()
        # Load torch model and feature extractor
        dguard_model = load_by_name(
            model_name=model_name, device=device, strict=True, loader=loader
        )
        self.model_name = model_name
        self.dguard_model = dguard_model
        self.model = dguard_model.embedding_model
        self.feature_extractor = dguard_model.feature_extractor
        self.resample_rate = dguard_model.sample_rate
        self.wavform_norm = dguard_model.wavform_normalize
        self.device = torch.device(device)

        self.vad = VAD()
        self.table = {}
        self.apply_vad = apply_vad
        # diarization parmas
        self.diar_num_spks = diar_num_spks
        self.diar_min_num_spks = diar_min_num_spks
        self.diar_max_num_spks = diar_max_num_spks
        self.diar_min_duration = diar_min_duration
        self.diar_window_secs = diar_window_secs
        self.diar_period_secs = diar_period_secs
        self.diar_frame_shift = diar_frame_shift
        self.diar_batch_size = diar_batch_size
        self.diar_subseg_cmn = diar_subseg_cmn

    def set_wavform_norm(self, wavform_norm: bool):
        self.wavform_norm = wavform_norm

    def set_resample_rate(self, resample_rate: int):
        self.resample_rate = resample_rate

    def set_vad(self, apply_vad: bool):
        self.apply_vad = apply_vad

    def set_gpu(self, device_id: int):
        if device_id >= 0:
            device = "cuda:{}".format(device_id)
        else:
            device = "cpu"
        self.device = torch.device(device)
        self.model = self.model.to(self.device)

    def set_diarization_params(
        self,
        num_spks=None,
        min_num_spks=1,
        max_num_spks=20,
        min_duration: float = 0.255,
        window_secs: float = 1.5,
        period_secs: float = 0.75,
        frame_shift: int = 10,
        batch_size: int = 32,
        subseg_cmn: bool = True,
    ):
        self.diar_num_spks = num_spks
        self.diar_min_num_spks = min_num_spks
        self.diar_max_num_spks = max_num_spks
        self.diar_min_duration = min_duration
        self.diar_window_secs = window_secs
        self.diar_period_secs = period_secs
        self.diar_frame_shift = frame_shift
        self.diar_batch_size = batch_size
        self.diar_subseg_cmn = subseg_cmn

    def compute_fbank(self, wavform, sample_rate, cmn):
        feat = self.feature_extractor(wavform)
        return feat

    def extract_embedding_feats(self, fbanks, batch_size, subseg_cmn):
        fbanks_array = np.stack(fbanks)
        if subseg_cmn:
            mean_value = np.mean(fbanks_array, axis=1, keepdims=True)
            fbanks_array = fbanks_array - mean_value
        embeddings = []
        fbanks_array = torch.from_numpy(fbanks_array).to(self.device)
        for i in tqdm(range(0, fbanks_array.shape[0], batch_size)):
            batch_feats = fbanks_array[i : i + batch_size]
            batch_embs = self.model(batch_feats)
            if isinstance(batch_embs, tuple):
                batch_embs = batch_embs[-1]
            else:
                batch_embs = batch_embs
            embeddings.append(batch_embs.detach().cpu().numpy())
        embeddings = np.vstack(embeddings)
        return embeddings

    def extract_embedding(self, audio_path: str):
        pcm, sample_rate = torchaudio.load(audio_path, normalize=self.wavform_norm)

        if self.apply_vad:
            print(f"Before VAD: {pcm.shape}")
            # #TODD :Refine the segments logic, here we just
            # suppose there is only silence at the start/end of the speech
            segments = self.vad.get_speech_timestamps(audio_path, return_seconds=True)
            pcmTotal = torch.Tensor()
            segments = list(segments)
            if len(segments) > 0:
                for segment in segments:
                    start = int(segment["start"] * sample_rate)
                    end = int(segment["end"] * sample_rate)
                    pcmTemp = pcm[0, start:end]
                    pcmTotal = torch.cat([pcmTotal, pcmTemp], 0)
                pcm = pcmTotal.unsqueeze(0)
            else:
                return None
            print(f"After VAD: {pcm.shape}")
        pcm = pcm.to(torch.float)
        if sample_rate != self.resample_rate:
            pcm = torchaudio.transforms.Resample(
                orig_freq=sample_rate, new_freq=self.resample_rate
            )(pcm)
        feats = self.compute_fbank(pcm, sample_rate=self.resample_rate, cmn=True)
        feats = feats.unsqueeze(0)
        feats = feats.to(self.device)
        self.model.eval()
        with torch.no_grad():
            outputs = self.model(feats)
            outputs = outputs[-1] if isinstance(outputs, tuple) else outputs
        embedding = outputs[0].to(torch.device("cpu"))
        return embedding

    def extract_embedding_list(self, scp_path: str):
        names = []
        embeddings = []
        with open(scp_path, "r") as read_scp:
            for line in tqdm(read_scp):
                name, wav_path = line.strip().split()
                names.append(name)
                embedding = self.extract_embedding(wav_path)
                embeddings.append(embedding.detach().numpy())
        return names, embeddings

    def compute_similarity(self, audio_path1: str, audio_path2: str) -> float:
        e1 = self.extract_embedding(audio_path1)
        e2 = self.extract_embedding(audio_path2)
        if e1 is None or e2 is None:
            return 0.0
        else:
            return self.cosine_similarity(e1, e2)

    def cosine_similarity(self, e1, e2, need_normalize=False):
        if isinstance(e1, np.ndarray):
            # calc cosine similarity by numpy
            if need_normalize:
                cosine_score = np.dot(e1, e2) / (np.linalg.norm(e1) * np.linalg.norm(e2))
            else:
                cosine_score = np.dot(e1, e2)
        elif isinstance(e1, torch.Tensor):
            if need_normalize:
                cosine_score = torch.dot(e1, e2) / (torch.norm(e1) * torch.norm(e2))
            else:
                cosine_score = torch.dot(e1, e2)
            cosine_score = cosine_score.item()
        elif isinstance(e1, list):
            e1 = np.array(e1)
            e2 = np.array(e2)
            if need_normalize:
                cosine_score = np.dot(e1, e2) / (np.linalg.norm(e1) * np.linalg.norm(e2))
            else:
                cosine_score = np.dot(e1, e2)
        else:
            raise ValueError(
                "Unsupported type for e1 and e2, should be numpy or torch or list"
            )
        return cosine_score
        # return (cosine_score + 1.0) / 2  # normalize: [-1, 1] => [0, 1]

    def register(self, name: str, audio_path: str):
        if name in self.table:
            print("Speaker {} already registered, ignore".format(name))
        else:
            self.table[name] = self.extract_embedding(audio_path)

    def recognize(self, audio_path: str):
        q = self.extract_embedding(audio_path)
        best_score = 0.0
        best_name = ""
        for name, e in self.table.items():
            score = self.cosine_similarity(q, e)
            if best_score < score:
                best_score = score
                best_name = name
        result = {}
        result["name"] = best_name
        result["confidence"] = best_score
        return result

    def diarize(self, audio_path: str, utt: str = "unk"):

        pcm, sample_rate = torchaudio.load(audio_path, normalize=False)
        # 1. vad
        vad_segments = self.vad.get_speech_timestamps(audio_path, return_seconds=True)

        # 2. extact fbanks
        subsegs, subseg_fbanks = [], []
        window_fs = int(self.diar_window_secs * 1000) // self.diar_frame_shift
        period_fs = int(self.diar_period_secs * 1000) // self.diar_frame_shift
        for item in vad_segments:
            begin, end = item["start"], item["end"]
            if end - begin >= self.diar_min_duration:
                begin_idx = int(begin * sample_rate)
                end_idx = int(end * sample_rate)
                tmp_wavform = pcm[0, begin_idx:end_idx].unsqueeze(0).to(torch.float)
                fbank = self.compute_fbank(
                    tmp_wavform, sample_rate=sample_rate, cmn=False
                )
                tmp_subsegs, tmp_subseg_fbanks = subsegment(
                    fbank=fbank,
                    seg_id="{:08d}-{:08d}".format(int(begin * 1000), int(end * 1000)),
                    window_fs=window_fs,
                    period_fs=period_fs,
                    frame_shift=self.diar_frame_shift,
                )
                subsegs.extend(tmp_subsegs)
                subseg_fbanks.extend(tmp_subseg_fbanks)

        # no speech segment, return empty list
        if len(subsegs) == 0:
            return []

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

        return merged_segment_to_labels

    def diarize_list(self, scp_path: str):
        utts = []
        segment2labels = []
        with open(scp_path, "r", encoding="utf-8") as read_scp:
            for line in tqdm(read_scp):
                utt, wav_path = line.strip().split()
                utts.append(utt)
                segment2label = self.diarize(wav_path, utt)
                segment2labels.append(segment2label)
        return utts, segment2labels

    def make_rttm(self, merged_segment_to_labels, outfile):
        with open(outfile, "w", encoding="utf-8") as fin:
            for utt, begin, end, label in merged_segment_to_labels:
                fin.write(
                    "SPEAKER {} {} {:.3f} {:.3f} <NA> <NA> {} <NA> <NA>\n".format(
                        utt, 1, float(begin), float(end) - float(begin), label
                    )
                )

    def vad(self, audio_path: str):
        pcm, sample_rate = torchaudio.load(audio_path, normalize=False)
        vad_segments = self.vad.get_speech_timestamps(audio_path, return_seconds=True)
        return vad_segments

    def vad_list(self, scp_path: str):
        vad_results = {}
        with open(scp_path, "r", encoding="utf-8") as read_scp:
            for line in tqdm(read_scp):
                utt, wav_path = line.strip().split()
                vad_results[utt] = self.vad(wav_path)
        return vad_results

    # Dguard
    def file_similarity_list(
        self, trial_list, length=-1, start_time=0, mean=False, vad=False
    ):
        # 参数解释
        # trial_list: 试音文件列表, 每个元素的格式为: (wav1, wav2) 或者 (wav1, wav2, id1, id2)， 如果没有id1和id2，则默认为None
        #               如果有id1和id2，则会将wav1和wav2的embedding存储在dguard_model.table中，下次计算时直接从self.table中取出
        # length: 截取的长度，单位为秒，如果为-1，则不截取
        # start_time: 截取的起始时间，单位为秒,如果为0，则从头开始截取，如果为1，则代表每条音频都会从第1秒开始截取
        # mean: 是否计算均值，如果为True，则计算所有切片（长度为length）embedding的均值，如果为False，则只利用首个切片作为模型输入
        #           例如如果原始音频长度为10s，mean=True，length=3s，start_time=0，则会截取0-3s，3-6s，6-9s三个切片，然后计算三个切片的embedding均值
        #           如果mean=False，则只会截取0-3s的切片，然后计算embedding
        return self.dguard_model.file_similarity_list(
            trial_list,
            length=length,
            start_time=start_time,
            mean=mean,
            vad=False,
        )

    def file_similarity(
        self,
        wav1,
        wav2,
        length=-1,
        start_time=0,
        mean=False,
        id1=None,
        id2=None,
        vad=False,
    ):
        # 参数解释
        # wav1, wav2: 两个音频文件的路径
        # id1, id2: 两个音频文件的id，如果不为None，则会将wav1和wav2的embedding存储在dguard_model.table中，下次计算时直接从self.table中取出
        # length: 截取的长度，单位为秒，如果为-1，则不截取
        # start_time: 截取的起始时间，单位为秒,如果为0，则从头开始截取，如果为1，则代表每条音频都会从第1秒开始截取
        # mean: 是否计算均值，如果为True，则计算所有切片（长度为length）embedding的均值，如果为False，则只利用首个切片作为模型输入
        #           例如如果原始音频长度为10s，mean=True，length=3s，start_time=0，则会截取0-3s，3-6s，6-9s三个切片，然后计算三个切片的embedding均值
        #           如果mean=False，则只会截取0-3s的切片，然后计算embedding
        return self.dguard_model.file_similarity(
            wav1,
            wav2,
            length=length,
            start_time=start_time,
            mean=mean,
            id1=id1,
            id2=id2,
            vad=False,
        )

    def dguard_extract_embedding(
        self, wav_path_list, length=-1, start_time=0, mean=False, vad=False
    ):
        # 参数解释
        # wav_path_list: 音频文件列表
        # length: 截取的长度，单位为秒，如果为-1，则不截取
        # start_time: 截取的起始时间，单位为秒,如果为0，则从头开始截取，如果为1，则代表每条音频都会从第1秒开始截取
        # mean: 是否计算均值，如果为True，则计算所有切片（长度为length）embedding的均值，如果为False，则只利用首个切片作为模型输入
        return self.encode_list(
            self,
            wav_path_list,
            length=length,
            start_time=start_time,
            mean=mean,
            vad=False,
        )

    def __repr__(self):
        return f"Speaker(model_name={self.model_name}, device={self.device})"


def load_dguard_model(model_name: str, device: str, loader: str) -> Speaker:
    if "_and_" in model_name:
        model_names = model_name.split("_and_")
        return [Speaker(m, device, loader) for m in model_names]
    else:
        return Speaker(model_name, device, loader)


def main():
    args = get_args()
    multi_model = False
    print("Loading model from D-Gurad ...")
    model_name = args.model_name
    device = args.device
    loader = args.loader
    model = load_dguard_model(model_name, device, loader)
    print(f"Model {model_name} loaded successfully")
    # print(model)
    if isinstance(model, list):
        multi_model = True
        print("Multiple models loaded")
        for i, m in enumerate(model):
            print(f"Model {i}: {m}")
            m.set_resample_rate(args.resample_rate)
            m.set_vad(args.vad)
            # m.set_gpu(args.gpu)
            m.set_diarization_params(
                num_spks=args.diar_num_spks,
                min_num_spks=args.diar_min_num_spks,
                max_num_spks=args.diar_max_num_spks,
                min_duration=args.diar_min_duration,
                window_secs=args.diar_window_secs,
                period_secs=args.diar_period_secs,
                frame_shift=args.diar_frame_shift,
                batch_size=args.diar_emb_bs,
                subseg_cmn=args.diar_subseg_cmn,
            )
    else:
        model.set_resample_rate(args.resample_rate)
        model.set_vad(args.vad)
        # model.set_gpu(args.gpu)
        model.set_diarization_params(
            num_spks=args.diar_num_spks,
            min_num_spks=args.diar_min_num_spks,
            max_num_spks=args.diar_max_num_spks,
            min_duration=args.diar_min_duration,
            window_secs=args.diar_window_secs,
            period_secs=args.diar_period_secs,
            frame_shift=args.diar_frame_shift,
            batch_size=args.diar_emb_bs,
            subseg_cmn=args.diar_subseg_cmn,
        )
    if args.task == "embedding":
        if multi_model:
            for i, m in enumerate(model):
                model_name = m.model_name
                embedding = m.extract_embedding(args.audio_file)
                if embedding is not None:
                    if args.output_file is None:
                        print(embedding)
                    else:
                        np.savetxt(
                            args.output_file + f"_{model_name}",
                            embedding.detach().numpy(),
                        )
                        print("Succeed, see {}".format(args.output_file + f"_{i}"))
                else:
                    print("Fails to extract embedding")
        else:
            embedding = model.extract_embedding(args.audio_file)
            if embedding is not None:
                if args.output_file is None:
                    print(embedding)
                else:
                    np.savetxt(args.output_file, embedding.detach().numpy())
                    print("Succeed, see {}".format(args.output_file))
            else:
                print("Fails to extract embedding")
    elif args.task == "embedding_kaldi":
        if multi_model:
            for _, m in enumerate(model):
                names, embeddings = m.extract_embedding_list(args.wav_scp)
                embed_ark = args.output_file + f"_{m.model_name}.ark"
                embed_scp = args.output_file + f"_{m.model_name}.scp"
                with kaldiio.WriteHelper(
                    "ark,scp:" + embed_ark + "," + embed_scp
                ) as writer:
                    for name, embedding in zip(names, embeddings):
                        writer(name, embedding)
        else:
            names, embeddings = model.extract_embedding_list(args.wav_scp)
            embed_ark = args.output_file + ".ark"
            embed_scp = args.output_file + ".scp"
            with kaldiio.WriteHelper(
                "ark,scp:" + embed_ark + "," + embed_scp
            ) as writer:
                for name, embedding in zip(names, embeddings):
                    writer(name, embedding)
    elif args.task == "similarity":
        if multi_model:
            scores = []
            for i, m in enumerate(model):
                score = m.compute_similarity(args.audio_file, args.audio_file2)
                scores.append(score)
                print(f"Model {i} similarity: {score}")
            print(f"Average similarity: {sum(scores) / len(scores)}")
        else:
            print(model.compute_similarity(args.audio_file, args.audio_file2))
    elif args.task == "diarization":
        diar_result = model.diarize(args.audio_file)
        if args.output_file is None:
            for _, start, end, spkid in diar_result:
                print("{:.3f}\t{:.3f}\t{:d}".format(start, end, spkid))
        else:
            model.make_rttm(diar_result, args.output_file)
    elif args.task == "diarization_list":
        utts, segment2labels = model.diarize_list(args.wav_scp)
        assert args.output_file is not None
        model.make_rttm(np.vstack(segment2labels), args.output_file)
    else:
        print("Unsupported task {}".format(args.task))
        sys.exit(-1)


if __name__ == "__main__":
    main()
