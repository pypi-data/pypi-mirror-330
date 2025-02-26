# coding = utf-8
# @Time    : 2024-12-16  16:47:57
# @Author  : zhaosheng@lyxxkj.com.cn
# @Describe: Encrypt the license file and ONNX model file.

import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


# 加密许可证文件
def encrypt_license(license_content, output_file, key):
    # mkdir
    backend = default_backend()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    # Padding data for encryption
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(license_content.encode()) + padder.finalize()
    with open(output_file, "wb") as f:
        f.write(iv)
        f.write(encryptor.update(padded_data) + encryptor.finalize())


# 加密ONNX模型文件
def encrypt_onnx_model(input_file, output_file, key):
    backend = default_backend()
    iv = os.urandom(16)  # 初始化向量
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()

    # 读取ONNX模型文件
    with open(input_file, "rb") as f:
        model_data = f.read()

    # 使用AES加密
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(model_data) + padder.finalize()

    with open(output_file, "wb") as f:
        f.write(iv)  # 写入初始化向量
        f.write(encryptor.update(padded_data) + encryptor.finalize())
