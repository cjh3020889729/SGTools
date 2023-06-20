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
import copy
import cv2
import numpy as np

from ..env.logger import create_logger
from ..env.register import register
logger=create_logger(log_name=__name__)

class BaseOperator:
    """预处理算子基类
    """
    def __init__(self, name='BaseOperator'):
        self._name=name
    
    def _apply_image(self, sample):
        NotImplementedError("Please Implement The Operator's({0}) _apply_image function!".format(self._name))

    def _apply_label(self, sample):
        NotImplementedError("Please Implement The Operator's({0}) _apply_label function!".format(self._name))

    def __call__(self, sample):
        _sample=copy.deepcopy(sample)
        _sample=self._apply_image(_sample)
        _sample=self._apply_label(_sample)
        return _sample

    def __str__(self) -> str:
        return self._name
    
    def __repr__(self) -> str:
        return self._name

@register
class EncodeImage(BaseOperator):
    """读取图像预处理
    """
    def __init__(self, image_path):
        super(EncodeImage, self).__init__("EncodeImage")
    
    def _apply_image(self, sample):
        pass

    def _apply_label(self, sample):
        pass

@register
class Normalize(BaseOperator):
    """归一化预处理
    """
    def __init__(self,
                 means=[127.5, 127.5, 127.5],
                 stds=[0, 0, 0]):
        super(Normalize, self).__init__("Normalize")
    
    def _apply_image(self, sample):
        pass

    def _apply_label(self, sample):
        pass

@register
class ResizeImage(BaseOperator):
    """图像缩放预处理
    """
    def __init__(self,
                 target_size=[32, 32],
                 by_short=False):
        super(ResizeImage, self).__init__("ResizeImage")
    
    def _apply_image(self, sample):
        pass

    def _apply_label(self, sample):
        pass

@register
class FlipImage(BaseOperator):
    """图像翻转预处理
    """
    def __init__(self,
                 flip_mode=0):
        super(FlipImage, self).__init__("FlipImage")
    
    def _apply_image(self, sample):
        pass

    def _apply_label(self, sample):
        pass

@register
class CenterCropImage(BaseOperator):
    """中心裁剪预处理
    """
    def __init__(self,
                 crop_size=[16, 16]):
        super(CenterCropImage, self).__init__("CenterCropImage")
    
    def _apply_image(self, sample):
        pass

    def _apply_label(self, sample):
        pass

@register
class RandomResizeImage(BaseOperator):
    """随机缩放预处理
    """
    def __init__(self):
        super(RandomResizeImage, self).__init__("RandomResizeImage")
    
    def _apply_image(self, sample):
        pass

    def _apply_label(self, sample):
        pass

@register
class RandomFlipImage(BaseOperator):
    """随机翻转预处理
    """
    def __init__(self):
        super(RandomFlipImage, self).__init__("RandomFlipImage")
    
    def _apply_image(self, sample):
        pass

    def _apply_label(self, sample):
        pass

@register
class RandomCropImage(BaseOperator):
    """随机裁剪预处理
    """
    def __init__(self):
        super(RandomCropImage, self).__init__("RandomCropImage")
    
    def _apply_image(self, sample):
        pass

    def _apply_label(self, sample):
        pass

logger.info("Transform Module is Loaded Successly!")