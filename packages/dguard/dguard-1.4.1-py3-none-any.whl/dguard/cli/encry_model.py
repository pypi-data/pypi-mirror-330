# coding = utf-8
# @Time    : 2024-12-16  16:15:42
# @Author  : zhaosheng@lyxxkj.com.cn
# @Describe: Encrypt the model file
# By using Fernet symmetric encryption algorithm

import base64
import getpass
import os

from cryptography.fernet import Fernet


def encrypt_model(model_path, output_path, key):
    # Read the original PyTorch model file
    with open(model_path, "rb") as f:
        model_bytes = f.read()

    # Create a Fernet object for encryption
    fernet = Fernet(key)

    # Encrypt the model
    encrypted_model = fernet.encrypt(model_bytes)

    # Save the encrypted model to the output path
    with open(output_path, "wb") as f:
        f.write(encrypted_model)

    print(f"Model has been encrypted and saved to {output_path}")


def encrypt_all(dirpath):
    # encrypt all yaml and pt file in the dirpath and
    # save to the same dir as "encrypted_" + filename
    # Get encryption key from user and prepare it
    key = getpass.getpass("Please input the key for encryption: ")
    key = key + "a" * (32 - len(key)) if len(key) < 32 else key[:32]
    key = base64.urlsafe_b64encode(key.encode())

    for filename in os.listdir(dirpath):
        if filename.endswith(".yaml") or filename.endswith(".pt"):
            encrypt_model(
                os.path.join(dirpath, filename),
                os.path.join(dirpath, "encrypted_" + filename),
                key,
            )
    print("All files have been encrypted.")
