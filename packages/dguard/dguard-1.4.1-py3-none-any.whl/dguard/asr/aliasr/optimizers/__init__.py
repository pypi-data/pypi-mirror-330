import torch

from dguard.asr.aliasr.optimizers.fairseq_adam import FairseqAdam
from dguard.asr.aliasr.optimizers.sgd import SGD

optim_classes = dict(
    adam=torch.optim.Adam,
    fairseq_adam=FairseqAdam,
    adamw=torch.optim.AdamW,
    sgd=SGD,
    adadelta=torch.optim.Adadelta,
    adagrad=torch.optim.Adagrad,
    adamax=torch.optim.Adamax,
    asgd=torch.optim.ASGD,
    lbfgs=torch.optim.LBFGS,
    rmsprop=torch.optim.RMSprop,
    rprop=torch.optim.Rprop,
)
