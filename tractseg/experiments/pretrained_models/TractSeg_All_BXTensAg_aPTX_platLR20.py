#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from tractseg.libs import exp_utils
from tractseg.experiments.tract_seg import Config as TractSegConfig


class Config(TractSegConfig):
    EXP_NAME = os.path.basename(__file__).split(".")[0]

    DATASET_FOLDER = "HCP_preproc_all"
    NR_OF_GRADIENTS = 18
    FEATURES_FILENAME = "32g270g_BX"
    P_SAMP = 0.4

    CLASSES = "AutoPTX_42"
    NR_OF_CLASSES = len(exp_utils.get_bundle_names(CLASSES)[1:])

    DATASET = "HCP_all"

    LR_SCHEDULE = True
    LR_SCHEDULE_MODE = "min"
    LR_SCHEDULE_PATIENCE = 20

    NUM_EPOCHS = 200    # 130 probably also fine
