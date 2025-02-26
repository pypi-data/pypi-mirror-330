#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Copyright FunASR (https://github.com/alibaba-damo-academy/FunASR). All Rights Reserved.
#  MIT License  (https://opensource.org/licenses/MIT)

import logging
import time
from contextlib import contextmanager
from distutils.version import LooseVersion
from typing import Dict, Optional, Tuple

import torch

from dguard.asr.aliasr.losses.label_smoothing_loss import LabelSmoothingLoss
from dguard.asr.aliasr.models.transducer.beam_search_transducer import (
    BeamSearchTransducer,
)
from dguard.asr.aliasr.models.transducer.model import Transducer
from dguard.asr.aliasr.models.transformer.scorers.ctc import CTCPrefixScorer
from dguard.asr.aliasr.models.transformer.scorers.length_bonus import LengthBonus
from dguard.asr.aliasr.models.transformer.utils.nets_utils import get_transducer_task_io
from dguard.asr.aliasr.register import tables
from dguard.asr.aliasr.train_utils.device_funcs import force_gatherable
from dguard.asr.aliasr.utils import postprocess_utils
from dguard.asr.aliasr.utils.datadir_writer import DatadirWriter
from dguard.asr.aliasr.utils.load_utils import (
    extract_fbank,
    load_audio_text_image_video,
)

if LooseVersion(torch.__version__) >= LooseVersion("1.6.0"):
    from torch.cuda.amp import autocast
else:
    # Nothing to do if torch<1.6.0
    @contextmanager
    def autocast(enabled=True):
        yield


@tables.register("model_classes", "BAT")  # TODO: BAT training
class BAT(Transducer):
    pass
