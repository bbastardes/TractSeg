import os
from tractseg.experiments.tract_seg_lowres import Config as TractSegConfig_LowRes

class Config(TractSegConfig_LowRes):
    EXP_NAME = os.path.basename(__file__).split(".")[0]

    INPUT_DIM = (80, 80)