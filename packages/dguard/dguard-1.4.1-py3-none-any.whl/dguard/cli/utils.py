# coding = utf-8
# @Time    : 2024-12-16  16:17:10
# @Author  : zhaosheng@lyxxkj.com.cn
# @Describe: Utils for CLI.

import argparse


def get_args():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "-t",
        "--task",
        choices=[
            "embedding",
            "embedding_kaldi",
            "similarity",
            "diarization",
            "diarization_list",
        ],
        default="embedding",
        help="task type",
    )
    parser.add_argument(
        "-l",
        "--language",
        choices=[
            "chinese",
            "english",
        ],
        default="chinese",
        help="language type",
    )
    # Dguard
    parser.add_argument(
        "--model_name",
        type=str,
        default="resnet293_cjsd8000_wespeaker_split",
        help="model name",
    )
    parser.add_argument("--device", type=str, default="cuda:0", help="device")
    parser.add_argument("--loader", type=str, default="wespeaker", help="Model loader")
    # parser.add_argument('-p',
    #                     '--pretrain',
    #                     type=str,
    #                     default="",
    #                     help='model directory')
    # parser.add_argument('-g',
    #                     '--gpu',
    #                     type=int,
    #                     default=-1,
    #                     help='which gpu to use (number <0 means using cpu)')
    parser.add_argument("--audio_file", help="audio file")
    parser.add_argument(
        "--audio_file2", help="audio file2, specifically for similarity task"
    )
    parser.add_argument(
        "--wav_scp",
        help="path to wav.scp, for extract and saving " "kaldi-stype embeddings",
    )
    parser.add_argument(
        "--resample_rate", type=int, default=16000, help="resampling rate"
    )
    parser.add_argument("--vad", action="store_true", help="whether to do VAD or not")
    parser.add_argument(
        "--output_file",
        default=None,
        help="output file to save speaker embedding " "or save diarization result",
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
        default=32,
        help="batch size for embedding extraction",
    )
    parser.add_argument(
        "--diar_subseg_cmn",
        type=bool,
        default=True,
        help="do cmn after or before fbank sub-segmentation",
    )
    args = parser.parse_args()
    return args
