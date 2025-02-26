# coding = utf-8
# @Time    : 2024-12-10  12:42:42
# @Author  : zhaosheng@lyxxkj.com.cn
# @Describe: Pickable session for VAD.

import os
from functools import partial

import onnxruntime as ort


class PickableSession:
    """
    This is a wrapper to make the current InferenceSession class pickable.
    """

    def __init__(self, onnx_path=None):
        # if onnx_path is None, load $DGUARD_MODEL_PATH/dguard_vad.onnx as default
        if onnx_path is None:
            DGUARD_MODEL_PATH = os.environ.get("DGUARD_MODEL_PATH")
            if not DGUARD_MODEL_PATH:
                raise ValueError(
                    "Please set the environment variable DGUARD_MODEL_PATH or specify the onnx_path."
                )
            onnx_path = os.path.join(DGUARD_MODEL_PATH, "dguard_vad.onnx")

        self.model_path = onnx_path
        
        # Initialize session options directly within InferenceSession constructor
        self.init_session = partial(
            ort.InferenceSession,
            providers=['CUDAExecutionProvider'],  # Use GPU if available , 'CPUExecutionProvider'
            provider_options=[{}],  # Default options for each provider
        )

        # Attempt to initialize the session with the model path
        try:
            self.sess = self.init_session(self.model_path)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize InferenceSession with model at {self.model_path}: {e}")

    def run(self, *args):
        return self.sess.run(None, *args)

    def __getstate__(self):
        return {"model_path": self.model_path}

    def __setstate__(self, values):
        self.model_path = values["model_path"]
        self.sess = self.init_session(self.model_path)


# Instantiate vad_session after ensuring that onnxruntime is correctly installed and configured
# try:
vad_session = PickableSession()
# except Exception as e:
#     print(f"An error occurred during initialization of vad_session: {e}")
#     vad_session = None