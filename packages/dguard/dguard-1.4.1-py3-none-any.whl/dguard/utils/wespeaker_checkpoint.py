# coding = utf-8
# @Time    : 2024-12-16  17:18:40
# @Author  : zhaosheng@lyxxkj.com.cn
# @Describe: Wespeaker Checkpoint.

import io
import logging

import torch
from cryptography.fernet import Fernet


def load_checkpoint(model: torch.nn.Module, path: str, encrypt=False, key=None):
    if encrypt:
        with open(path, "rb") as f:
            encrypted_data = f.read()
        decrypted_data = Fernet(key).decrypt(encrypted_data)
        b = io.BytesIO(decrypted_data)
        checkpoint = torch.load(b, map_location="cpu")
    else:
        checkpoint = torch.load(path, map_location="cpu")
    missing_keys, unexpected_keys = model.load_state_dict(checkpoint, strict=False)
    for key in missing_keys:
        logging.warning("missing tensor: {}".format(key))
    for key in unexpected_keys:
        logging.warning("unexpected tensor: {}".format(key))


def save_checkpoint(model: torch.nn.Module, path: str):
    if isinstance(model, torch.nn.DataParallel):
        state_dict = model.module.state_dict()
    elif isinstance(model, torch.nn.parallel.DistributedDataParallel):
        state_dict = model.module.state_dict()
    else:
        state_dict = model.state_dict()
    torch.save(state_dict, path)
