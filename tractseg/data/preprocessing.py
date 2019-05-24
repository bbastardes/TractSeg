# Copyright 2017 Division of Medical Image Computing, German Cancer Research Center (DKFZ)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Run this script to crop images + segmentations to brain area. Then save as nifti.
Reduces datasize and therefore IO by at least two times.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
from os.path import join
import nibabel as nib
import numpy as np
from joblib import Parallel, delayed

from tractseg.libs.system_config import SystemConfig as C
from tractseg.libs import dataset_utils
from tractseg.libs.subjects import get_all_subjects
from tractseg.libs import exp_utils

#todo: adapt
dataset = "HCP_BLANCA"
DATASET_FOLDER = "data_training"  # source folder
DATASET_FOLDER_PREPROC = "data_preproc"  # target folder

# dataset = "HCP_all"
# DATASET_FOLDER = "HCP_for_training_COPY_all"  # source folder
# DATASET_FOLDER_PREPROC = "HCP_preproc_all"  # target folder


def create_preprocessed_files(subject):

    # todo: adapt
    # filenames_data = ["12g_125mm_peaks", "90g_125mm_peaks", "270g_125mm_peaks", "125mm_bedpostx_tensor"]
    # filenames_seg = ["bundle_masks_72", "bundle_peaks_Part1", "bundle_masks_dm",
    #                  "bundle_masks_autoPTX_dm", "bundle_masks_autoPTX_thr001"]

    # filenames_data = ["270g_125mm_peaks", "90g_125mm_peaks", "12g_125mm_peaks",
    #                   "12g_125mm_bedpostx_peaks_scaled", "90g_125mm_bedpostx_peaks_scaled",
    #                   "270g_125mm_bedpostx_peaks_scaled"]

    # filenames_data = ["270g_125mm_bedpostx_peaks_scaled", "32g_125mm_bedpostx_peaks_scaled"]
    # filenames_seg = ["bundle_masks_autoPTX_dm", "bundle_masks_autoPTX_thr001"]
    filenames_data = ["peaks", "nodif_brain_mask"]
    filenames_seg = ["bundle_masks_AR"]


    print("idx: {}".format(subjects.index(subject)))
    exp_utils.make_dir(join(C.DATA_PATH, DATASET_FOLDER_PREPROC, subject))

    for idx, filename in enumerate(filenames_data):
        path = join(C.NETWORK_DRIVE, DATASET_FOLDER, subject, filename + ".nii.gz")
        if os.path.exists(path):
            img = nib.load(path)
            data = img.get_data()
            affine = img.get_affine()
            data = np.nan_to_num(data)

            if idx == 0:
                data, _, bbox, _ = dataset_utils.crop_to_nonzero(data)
            else:
                data, _, _, _ = dataset_utils.crop_to_nonzero(data, bbox=bbox)

            # if idx > 0:
            # np.save(join(C.DATA_PATH, DATASET_FOLDER_PREPROC, subject, filename + ".npy"), data)
            nib.save(nib.Nifti1Image(data, affine), join(C.DATA_PATH, DATASET_FOLDER_PREPROC, subject,
                                                         filename + ".nii.gz"))
        else:
            print("skipping file: {}-{}".format(subject, idx))
            raise IOError("File missing")

    for filename in filenames_seg:
        data = nib.load(join(C.NETWORK_DRIVE, DATASET_FOLDER, subject, filename + ".nii.gz")).get_data()
        data, _, _, _ = dataset_utils.crop_to_nonzero(data, bbox=bbox)
        # np.save(join(C.DATA_PATH, DATASET_FOLDER_PREPROC, subject, filename + ".npy"), data)
        nib.save(nib.Nifti1Image(data, affine), join(C.DATA_PATH, DATASET_FOLDER_PREPROC, subject, filename +
                                                     ".nii.gz"))


if __name__ == "__main__":
    print("Output folder: {}".format(DATASET_FOLDER_PREPROC))
    subjects = get_all_subjects(dataset=dataset)
    Parallel(n_jobs=12)(delayed(create_preprocessed_files)(subject) for subject in subjects)  # 37
