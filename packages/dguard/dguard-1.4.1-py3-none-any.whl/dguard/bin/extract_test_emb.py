import argparse
import os
import random
import sys

import numpy as np
import torch
import torchaudio
from kaldiio import WriteHelper
from tqdm import tqdm

from dguard import DguardModel
from dguard.interface.models_info import model_info
from dguard.interface.pretrained import load_by_name
from dguard.speaker.utils.utils import set_seed
from dguard.utils.fileio import load_wav_scp
from dguard.utils.utils import get_logger

parser = argparse.ArgumentParser(description="Extract embeddings for evaluation.")
parser.add_argument("--exp_dir", default="", type=str, help="Exp dir")
parser.add_argument("--data", default="", type=str, help="Data dir")
parser.add_argument("--model_name", default="", type=str, help="model_name")
parser.add_argument("--seed", default=123, type=int, help="seed")
parser.add_argument("--length", default=3.0, type=float, help="wav length")
parser.add_argument("--start_from", default=0.0, type=float, help="start from(s)")
parser.add_argument("--use_gpu", action="store_true", help="Use gpu or not")
parser.add_argument("--gpu", nargs="+", help="GPU id to use.")


def main():
    args = parser.parse_args(sys.argv[1:])
    set_seed(args.seed)
    rank = int(os.environ["LOCAL_RANK"])
    world_size = int(os.environ["WORLD_SIZE"])
    embedding_dir = os.path.join(args.exp_dir, "embeddings")
    os.makedirs(embedding_dir, exist_ok=True)
    logger = get_logger(fpath=os.path.join(embedding_dir, "extract_emb.log"))

    if args.use_gpu:
        if torch.cuda.is_available():
            gpu = int(args.gpu[rank % len(args.gpu)])
            device = torch.device("cuda", gpu)
        else:
            msg = "No cuda device is detected. Using the cpu device."
            if rank == 0:
                logger.warning(msg)
            device = torch.device("cpu")
    else:
        device = torch.device("cpu")

    if "_and_" in args.model_name:
        MODELS = args.model_name.split("_and_")
        data = load_wav_scp(args.data)
        data_k = list(data.keys())
        local_k = data_k[rank::world_size]
        if len(local_k) == 0:
            logger.error("The number of threads exceeds the number of files")
            sys.exit()

        for _index in range(len(MODELS)):
            now_model = MODELS[_index]
            now_model_info = model_info[now_model]
            now_model_loader = now_model_info["mode"]
            dguard_model = DguardModel(
                model_name=now_model,
                device=device,
                strict=True,
                loader=now_model_loader,
            )
            model = dguard_model.embedding_model
            feature_extractor = dguard_model.feature_extractor
            emb_ark = os.path.join(
                embedding_dir,
                f"fusion_{now_model}_" + "xvector_%02d.ark" % rank,
            )
            emb_scp = os.path.join(
                embedding_dir,
                f"fusion_{now_model}_" + "xvector_%02d.scp" % rank,
            )
            if rank == 0:
                logger.info("Start extracting embeddings.")

            with WriteHelper(f"ark,scp:{emb_ark},{emb_scp}") as writer:
                for k in tqdm(local_k):
                    wav_path = data[k]
                    wav, fs = torchaudio.load(wav_path)
                    random_start = random.randint(
                        args.start_from, int(wav.shape[1] / fs) - args.length
                    )
                    embs = dguard_model.interface(
                        wav_path=wav_path,
                        length=args.length,
                        start_time=random_start,
                    )
                    print(f"emb shape: {embs[0].shape}")
                    emb = emb[0].detach().cpu().numpy()
                    writer(k, emb)

    else:
        now_model_info = model_info[args.model_name]
        dguard_model = load_by_name(
            model_name=args.model_name,
            device=device,
            strict=True,
            loader=now_model_info["mode"],
        )
        model = dguard_model.embedding_model

        data = load_wav_scp(args.data)
        data_k = list(data.keys())
        local_k = data_k[rank::world_size]
        if len(local_k) == 0:
            msg = "The number of threads exceeds the number of files"
            logger.info(msg)
            sys.exit()

        emb_ark = os.path.join(embedding_dir, "xvector_%02d.ark" % rank)
        emb_scp = os.path.join(embedding_dir, "xvector_%02d.scp" % rank)
        if rank == 0:
            logger.info("Start extracting embeddings.")

        with WriteHelper(f"ark,scp:{emb_ark},{emb_scp}") as writer:
            for k in tqdm(local_k):
                wav_path = data[k]
                wav, fs = torchaudio.load(wav_path)
                random_start = random.randint(
                    args.start_from, int(wav.shape[1] / fs) - args.length
                )

                embs = dguard_model.interface(
                    wav_path=wav_path,
                    length=args.length,
                    start_time=random_start,
                )
                print(f"emb shape: {embs[0].shape}")
                emb = embs[0].detach().cpu().numpy()
                emb = np.concatenate((emb, emb, emb), axis=1)
                emb = emb.reshape(-1)
                writer(k, emb)


if __name__ == "__main__":
    main()
