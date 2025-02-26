"""
Descripttion:
version: 1.0.1
Author: duanyibo 444689158@qq.com
Date: 2024-12-17 13:43:25
LastEditors: duanyibo 444689158@qq.com
LastEditTime: 2024-12-17 14:46:24
"""

import torch

from dguard.asv.dfaudio_model.model.loss import OCSoftmax
from dguard.asv.dfaudio_model.model.tdnn import TDNN

default_args = {
    "feature_type": "LFCC",
    "feature_dim": 60,
    "enc_dim": 256,
    "device": "cuda",
    "pooling_way": "ASP",
    "conv_way": "Res2block",
    "context": True,
    "channel": 512,
    "num_epochs": 100,
    "test_batch_size": 32,
    "test_step": 1,
    "epoch": 0,
    "lr": 0.0005,
    "lr-decay": 0.5,
    "interval": 30,
    "beta_1": 0.9,
    "beta_2": 0.999,
    "eps": 1e-8,
    "gpu": "3,5,6,7",
    "num_workers": 4,
    "seed": 688,
    "r_real": 0.9,
    "r_fake": 0.2,
    "alpha": 20,
    "model_path": "/home/duanyibo/dyb/Asvspoof/ECAPA-TDNN-OCloss_ASVspoof/ecapa-tdnn-ocloss-asvspoof/models_2024110/Res2block-ASP-feat/model_018.pt",
    "ocsoftmax": "/home/duanyibo/dyb/Asvspoof/ECAPA-TDNN-OCloss_ASVspoof/ecapa-tdnn-ocloss-asvspoof/models_2024110/Res2block-ASP-oc/model_018.pt",
    "wav_path": None,
}


class dfaudio_model:
    def __init__(self, feat_model_path, oc_model_path, device):
        """
        初始化模型加载器，加载TDNN和OCSoftmax模型。

        Args:
            feat_model_path (str): 特征提取模型的路径。
            oc_model_path (str): OCSoftmax模型的路径。
            device (str): 设备（'cuda' 或 'cpu'）。
            default_args (dict): 默认的参数字典。
        """
        self.device = device

        # 初始化 TDNN 模型
        self.feat_model = TDNN(
            **default_args,
        ).to(device)

        # 初始化 OCSoftmax 模型
        self.ocsoftmax = OCSoftmax(
            **default_args,
        ).to(device)

        # 加载模型权重
        self._load_models(feat_model_path, oc_model_path)

    def _load_models(self, feat_model_path, oc_model_path):
        """
        加载模型的状态字典，并设置模型为评估模式。
        """
        try:
            # 加载 TDNN 模型权重
            self.feat_model.load_state_dict(
                torch.load(feat_model_path, map_location=self.device)
            )
            self.feat_model.eval()  # 设置为评估模式
            self.feat_model.to(self.device)  # 移动到指定设备

            # 加载 OCSoftmax 模型权重
            self.ocsoftmax.load_state_dict(
                torch.load(oc_model_path, map_location=self.device)
            )
            self.ocsoftmax.eval()  # 设置为评估模式
            self.ocsoftmax.to(self.device)  # 移动到指定设备

        except Exception as e:
            print(f"Error loading models: {e}")
            raise e

    def get_models(self):
        """
        返回加载的模型。

        Returns:
            feat_model (TDNN): 加载的特征提取模型。
            ocsoftmax (OCSoftmax): 加载的 OCSoftmax 模型。
        """
        return self.feat_model, self.ocsoftmax
