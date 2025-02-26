import logging

import torch

from dguard.asr.aliasr.models.transformer.model import Transformer
from dguard.asr.aliasr.register import tables


@tables.register("model_classes", "Conformer")
class Conformer(Transformer):
    """CTC-attention hybrid Encoder-Decoder model"""

    def __init__(
        self,
        *args,
        **kwargs,
    ):

        super().__init__(*args, **kwargs)
