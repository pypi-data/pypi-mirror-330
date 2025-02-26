# coding = utf-8
# @Time    : 2024-12-16  16:47:27
# @Author  : zhaosheng@lyxxkj.com.cn
# @Describe: CLI for dguard.

from dguard.cli.encry_model import encrypt_all, encrypt_model
from dguard.cli.info import VERSION
from dguard.cli.info import main as print_info
from dguard.cli.speaker import Speaker, load_dguard_model
from dguard.cli.utils import get_args

__all__ = [
    "encrypt_all",
    "encrypt_model",
    "VERSION",
    "print_info",
    "get_args",
    "Speaker",
    "load_dguard_model",
]
