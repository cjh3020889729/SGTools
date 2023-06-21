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
import os, sys
import cv2
import numpy as np
from typing import List, Any

from ..env.logger import create_logger
from ..env.register import register
logger=create_logger(log_name=__name__)

@register
class BatchCompose:
    """批量预处理组合器
    """
    def __init__(self, transforms: List[Any]=[]):
        """
            transforms: 由批量预处理组成的列表
        """
        self._name="BatchCompose"
        self._transforms=transforms
    
    def __call__(self, samples):
        for _t in self._transforms:
            samples=_t(samples)
        batch_data={}
        for k in samples[0].keys():
            _data=[]
            for _sample in samples:
                _data.append(_sample[k])
            _data=np.stack(_data, axis=0)
            batch_data[k]=_data
        return batch_data

    def __str__(self) -> str:
        return self._name
    
    def __repr__(self) -> str:
        return self._name


logger.info("Batch Transform Module is Loaded Successly!")