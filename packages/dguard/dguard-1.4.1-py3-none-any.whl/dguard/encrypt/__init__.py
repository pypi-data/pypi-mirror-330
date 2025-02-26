# coding = utf-8
# @Time    : 2024-12-16  16:47:43
# @Author  : zhaosheng@lyxxkj.com.cn
# @Describe: Encrypt the license file and ONNX model file.

from dguard.encrypt.encrypt_license import encrypt_license, encrypt_onnx_model

__all__ = [
    "encrypt_license",
    "encrypt_onnx_model",
]
