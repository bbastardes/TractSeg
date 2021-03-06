import os
from tractseg.experiments.tract_seg import Config as TractSegConfig


class Config(TractSegConfig):
    EXP_NAME = os.path.basename(__file__).split(".")[0]

    FEATURES_FILENAME = "T1_Peaks12g90g270g"
    NR_OF_GRADIENTS = 10

    NORMALIZE_PER_CHANNEL = True
