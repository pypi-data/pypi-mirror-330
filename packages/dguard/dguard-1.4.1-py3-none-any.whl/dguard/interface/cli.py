# coding = utf-8
# @Time    : 2024-12-16  16:51:21
# @Author  : zhaosheng@lyxxkj.com.cn
# @Describe: This is Terminal Interface for dguard by pypi package

import argparse
import os

import torchaudio

from dguard import DguardModel as dm
from dguard.cli import print_info
from dguard.utils.dguard_model_utils import ALL_MODELS


def get_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "-t",
        "--task",
        choices=[
            "embedding",
            "embedding_list",
            "similarity",
            "similarity_list",
            "diarization",
            "vad",
            "vad_list",
            "info",
        ],
        default="embedding",
        help="task to do",
    )
    # Dguard
    parser.add_argument(
        "--model_names",
        type=str,
        default="dguard_sv_r101_cjsd8000_split_lm,dguard_sv_r152_cjsd8000_split_lm",
        help="model names split by ,",
    )
    parser.add_argument("--device", type=str, default="cuda:0", help="device to use")

    parser.add_argument("--audio_file", help="audio file for task")
    parser.add_argument(
        "--audio_file2", help="audio file2, specifically for similarity task"
    )

    parser.add_argument(
        "--wav_scp",
        help="path to wav.scp, for extract and saving kaldi-stype embeddings",
    )

    parser.add_argument("--channel", type=int, default=0, help="channel of audio file")

    parser.add_argument("--max_split_num", type=int, default=5, help="max split number")

    parser.add_argument(
        "--start_time",
        type=float,
        default=0,
        help="start time of audio segment",
    )

    parser.add_argument(
        "--mean",
        action="store_true",
        default=False,
        help="whether to do mean or not",
    )

    parser.add_argument(
        "--apply_vad",
        action="store_true",
        default=False,
        help="whether to do VAD or not",
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="whether to show verbose or not",
    )

    parser.add_argument(
        "--vad_min_duration", type=float, default=0.25, help="VAD min duration"
    )
    parser.add_argument(
        "--vad_smooth_threshold",
        type=float,
        default=0.25,
        help="VAD smooth threshold",
    )

    parser.add_argument(
        "--output_file",
        default=None,
        help="output file to save speaker embedding " "or save diarization result",
    )
    parser.add_argument(
        "--length",
        type=int,
        default=-1,
        help="length of audio segment, -1 means whole audio",
    )
    # diarization params
    parser.add_argument(
        "--diar_num_spks", type=int, default=None, help="number of speakers"
    )
    parser.add_argument(
        "--diar_min_num_spks",
        type=int,
        default=1,
        help="minimum number of speakers",
    )
    parser.add_argument(
        "--diar_max_num_spks",
        type=int,
        default=20,
        help="maximum number of speakers",
    )
    parser.add_argument(
        "--diar_min_duration",
        type=float,
        default=0.255,
        help="VAD min duration",
    )
    parser.add_argument(
        "--diar_window_secs",
        type=float,
        default=1.5,
        help="the window seconds in embedding extraction",
    )
    parser.add_argument(
        "--diar_period_secs",
        type=float,
        default=0.75,
        help="the shift seconds in embedding extraction",
    )
    parser.add_argument(
        "--diar_frame_shift",
        type=int,
        default=10,
        help="frame shift in fbank extraction (ms)",
    )
    parser.add_argument(
        "--diar_emb_bs",
        type=int,
        default=4,
        help="batch size for embedding extraction",
    )
    parser.add_argument(
        "--diar_subseg_cmn",
        type=bool,
        default=True,
        help="do cmn after or before fbank sub-segmentation",
    )
    parser.add_argument(
        "--clean_mode",
        action="store_true",
        default=False,
        help="Just print result without any other information",
    )
    parser.add_argument(
        "--vad_output_file",
        default=None,
        help="output file to save vad result (for `vad` task)",
    )
    parser.add_argument(
        "--vad_output_folder",
        default=None,
        help="output folder to save vad result (for `vad_list` task)",
    )
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    if args.clean_mode:
        args.verbose = False
    if args.task == "info":
        print_info()
    else:
        models = args.model_names.split(",")
        # print(models)
        for model in models:
            assert model in ALL_MODELS, f"Model {model} not implemented."

        model = dm(
            embedding_model_names=models,
            device=args.device,
            length=args.length,
            channel=args.channel,
            max_split_num=args.max_split_num,
            start_time=args.start_time,
            mean=args.mean,
            verbose=args.verbose,
            apply_vad=args.apply_vad,
            vad_min_duration=args.vad_min_duration,
            vad_smooth_threshold=args.vad_smooth_threshold,
            save_vad_path=None,
            diar_num_spks=args.diar_num_spks,
            diar_min_num_spks=args.diar_min_num_spks,
            diar_max_num_spks=args.diar_max_num_spks,
            diar_min_duration=args.diar_min_duration,
            diar_window_secs=args.diar_window_secs,
            diar_period_secs=args.diar_period_secs,
            diar_frame_shift=args.diar_frame_shift,
            diar_batch_size=args.diar_emb_bs,
            diar_subseg_cmn=args.diar_subseg_cmn,
        )
    if args.task == "embedding":
        embedding = model.encode(args.audio_file)
        embedding_str = " ".join(embedding.detach().cpu().numpy().astype(str))
        if args.output_file is None:
            if args.clean_mode:
                print(embedding_str)
            else:
                print(f"{args.audio_file} {embedding_str}")
        else:
            # save to text file
            with open(args.output_file, "w") as f:
                f.write(f"{args.audio_file} {embedding_str}\n")

    elif args.task == "embedding_list":
        # wav_scp file format:
        # utt_id wav_path
        with open(args.wav_scp, "r") as f:
            lines = f.readlines()
        files = [line.strip().split()[1] for line in lines]
        names = [line.strip().split()[0] for line in lines]
        embeddings = model.encode_list(files)
        embedding_strs = [
            " ".join(embedding.detach().cpu().numpy().astype(str))
            for embedding in embeddings
        ]
        if args.output_file is None:
            for name, embedding_str in zip(names, embedding_strs):
                if args.clean_mode:
                    print(embedding_str)
                else:
                    print(name, embedding_str)
        else:
            with open(args.output_file, "w") as f:
                for name, embedding_str in zip(names, embedding_strs):
                    f.write(f"{name} {embedding_str}\n")

    elif args.task == "similarity":
        sim = model.file_similarity(args.audio_file, args.audio_file2)
        result = ""
        for model_name in sim["scores"]:
            result += f"{model_name}:{sim['scores'][model_name]:.4f} "
        mean_score = sim["mean_score"]
        result += f"mean_score:{mean_score:.4f}"
        if args.output_file is None:
            if args.clean_mode:
                print(f"{mean_score:.4f}")
            else:
                print(f"{args.audio_file} {args.audio_file2} {result}\n")
        else:
            with open(args.output_file, "w") as f:
                f.write(f"{args.audio_file} {args.audio_file2} {result}\n")

    elif args.task == "similarity_list":
        # wav_scp file format:
        # utt_id1 wav_path1 utt_id2 wav_path2
        with open(args.wav_scp, "r") as f:
            lines = f.readlines()
        files = [[line.strip().split()[1], line.strip().split()[3]] for line in lines]
        names = [
            line.strip().split()[0] + "&" + line.strip().split()[2] for line in lines
        ]
        sims = model.file_similarity_list(files)
        if args.output_file is None:
            for name, sim in zip(names, sims):
                result = ""
                for model_name in sim["scores"]:
                    result += f"{model_name}:{sim['scores'][model_name]:.4f} "
                mean_score = sim["mean_score"]
                result += f"mean_score:{mean_score:.4f}"

                if args.clean_mode:
                    print(f"{mean_score:.4f}")
                else:
                    print(name, result)
        else:
            with open(args.output_file, "w") as f:
                for name, sim in zip(names, sims):
                    result = ""
                    for model_name in sim["scores"]:
                        result += f"{model_name}:{sim['scores'][model_name]:.4f} "
                    mean_score = sim["mean_score"]
                    result += f"mean_score:{mean_score:.4f}"
                    f.write(f"{name} {result}\n")

    elif args.task == "diarization":
        diar_result = model.diarize(args.audio_file)
        if args.output_file is None:
            print(diar_result)
        else:
            model.make_rttm(diar_result, args.output_file)

    elif args.task == "vad":
        vad_result = model.vad_file(args.audio_file)
        pcm = vad_result["pcm"]
        sample_rate = vad_result["sample_rate"]
        segments = vad_result["segments"]
        segments_str = ",".join(
            [f"{segment['start']:.2f}-{segment['end']:.2f}" for segment in segments]
        )
        if args.vad_output_file is None:
            pass
        else:
            with open(args.vad_output_file, "w") as f:
                torchaudio.save(args.vad_output_file, pcm, sample_rate)
                print(f"Save vad result to {args.vad_output_file}")
        if args.output_file is None:
            if args.clean_mode:
                print(segments_str)
            else:
                print(f"{args.audio_file} {segments_str}")
        else:
            with open(args.output_file, "w") as f:
                f.write(f"{args.audio_file} {segments_str}\n")

    elif args.task == "vad_list":
        with open(args.wav_scp, "r") as f:
            lines = f.readlines()
        files = [line.strip().split()[1] for line in lines]
        names = [line.strip().split()[0] for line in lines]
        with open(args.output_file, "w") as _f:
            for name, file in zip(names, files):
                vad_result = model.vad_file(file)
                pcm = vad_result["pcm"]
                sample_rate = vad_result["sample_rate"]
                segments = vad_result["segments"]
                segments_str = ",".join(
                    [
                        f"{segment['start']:.2f}-{segment['end']:.2f}"
                        for segment in segments
                    ]
                )
                if args.vad_output_folder is None:
                    pass
                else:
                    os.makedirs(args.vad_output_folder, exist_ok=True)
                    f = f"{args.vad_output_folder}/{name}.wav"
                    torchaudio.save(f, pcm, sample_rate)
                    print(f"Save vad result to {args.vad_output_folder}/{name}.wav")
                if args.output_file is None:
                    if args.clean_mode:
                        print(segments_str)
                    else:
                        print(f"{name} {segments_str}")
                else:
                    _f.write(f"{name} {segments_str}\n")
