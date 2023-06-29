# Copyright (c) 2023 SGTools Authors. All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os, sys, six
import numpy as np
import cv2
from typing import List, Any
from copy import deepcopy
from time import time

from sgt.datasets.base import BaseDataset

from ..env.logger import create_logger
from ..env.register import register
logger=create_logger(log_name=__name__)

__all__=[
    'NormalDataset',
    'TrainNormalDataset',
    'EvalNormalDataset'
]

from ..datasets.base import BaseDataset

class NormalDataset(BaseDataset):
    def __init__(self,
                 data_dir: str,
                 data_txt: str,
                 is_train_or_eval: bool = True):
        super(NormalDataset, self).__init__(
                            data_dir,
                            data_txt,
                            is_train_or_eval
                        )
    
    def parse_dataset(self) -> None:
        """解析data_txt添加样本图像path列表
            self._images
            self._labels
        """
        if not os.path.exists(os.path.join(self._data_dir, self._data_txt)):
            logger.error(
                "The Dataset data_txt path({0}) is not exists!".format(os.path.join(self._data_dir, self._data_txt)),
                stack_info=True
            )
            exit(1)
        _start_time=time()
        logger.info("The Normal Dataset Mode: {0}.".format('Train' if self._is_train_or_eval else 'Eval'))
        _images=[]
        _labels=[]
        with open(os.path.join(self._data_dir, self._data_txt), 'r') as f:
            logger.info("The Normal Dataset Has Load data_txt: {0}.".format(self._data_txt))
            _lines=f.readlines()
            for _l in _lines:
                _img, _lab = _l.split(' ')[:2]
                _img=os.path.join(self._data_dir, _img.strip())
                _lab=os.path.join(self._data_dir, _lab.strip())
                _images.append(_img)
                _labels.append(_lab)
        self._images=_images
        self._labels=_labels
        logger.info("The Normal Dataset Has Collect Image samples: {0}.".format(len(_images)))
        logger.info("The Normal Dataset Has Collect Label samples: {0}.".format(len(_labels)))
        logger.info("The Normal Dataset Load Data Cost Time: {0} s.".format(time()-_start_time))

@register
class TrainNormalDataset(NormalDataset):
    def __init__(self,
                 data_dir: str,
                 data_txt: str):
        super(TrainNormalDataset, self).__init__(
                            data_dir,
                            data_txt,
                            True
                        )

@register
class EvalNormalDataset(NormalDataset):
    def __init__(self,
                 data_dir: str,
                 data_txt: str):
        super(TrainNormalDataset, self).__init__(
                            data_dir,
                            data_txt,
                            False
                        )

logger.info("Normal Dataset Module is Loaded Successly!")