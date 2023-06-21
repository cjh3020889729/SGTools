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
from copy import deepcopy
from typing import List, Any

from ..env.logger import create_logger
from ..env.register import register
logger=create_logger(log_name=__name__)

__all__=[
    'EncodeImage',
    'Normalize',
    'ResizeImage',
    'FlipImage'
]

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
        _sample=deepcopy(sample)
        _sample=self._apply_image(_sample)
        _sample=self._apply_label(_sample)
        return _sample

    def __str__(self) -> str:
        return self._name
    
    def __repr__(self) -> str:
        return self._name

@register
class Compose:
    """预处理组合器
    """
    def __init__(self, transforms: List[Any]=[]):
        """
            transforms: 由预处理组成的列表
        """
        self._name="Compose"
        self._transforms=transforms
    
    def __call__(self, sample):
        _sample=deepcopy(sample)
        for _t in self._transforms:
            _sample=_t(_sample)
        return _sample

    def __str__(self) -> str:
        return self._name
    
    def __repr__(self) -> str:
        return self._name

@register
class EncodeImage(BaseOperator):
    """读取图像预处理
        sample base data struct:
            {
                'image_path': str,
                'label_path': str,
                # add image + image_shape
                'image': numyp.ndarray,
                'image_shape': list,
                # add label + label_shape
                'label': numyp.ndarray,
                'label_shape': list,
            }
    """
    def __init__(self, to_rgb=False):
        super(EncodeImage, self).__init__("EncodeImage")
        self._to_rgb=to_rgb
    
    def _apply_image(self, sample):
        _img_path=sample['image_path']
        _img=cv2.imread(_img_path)
        if self._to_rgb:
            _img=cv2.cvtColor(_img, cv2.COLOR_BGR2RGB)
        sample['image']=_img
        if len(_img.shape) == 2:
            sample['image_shape']=[_img.shape[0], _img.shape[1], 1] # H, W, C
        else:
            sample['image_shape']=list(_img.shape) # H, W, C
        del sample['image_path']
        return sample

    def _apply_label(self, sample):
        _img_path=sample['label_path']
        _img=cv2.imread(_img_path)
        if self._to_rgb:
            _img=cv2.cvtColor(_img, cv2.COLOR_BGR2RGB)
        sample['label']=_img
        if len(_img.shape) == 2:
            sample['label_shape']=[_img.shape[0], _img.shape[1], 1] # H, W, C
        else:
            sample['label_shape']=list(_img.shape) # H, W, C
        del sample['label_path']
        return sample

@register
class Normalize(BaseOperator):
    """归一化预处理
        sample base data struct:
            {
                'image_path': str,
                'label_path': str,
                'image': numyp.ndarray,
                'image_shape': list,
                'label': numyp.ndarray,
                'label_shape': list,
            }
    """
    def __init__(self,
                 means=[127.5, 127.5, 127.5],
                 stds=[127.5, 127.5, 127.5]):
        """初始化函数
            means: 归一化各通道的均值参数
            stds: 归一化各通道的标准方差参数
        """
        super(Normalize, self).__init__("Normalize")
        self._means=np.asarray(means)
        self._stds=np.asarray(stds)
    
    def _apply_image(self, sample):
        _img=sample['image'].astype('float32')
        _img-=self._means
        _img/=self._stds
        sample['image']=_img
        return sample

    def _apply_label(self, sample):
        _img=sample['label'].astype('float32')
        _img-=self._means
        _img/=self._stds
        sample['label']=_img
        return sample

@register
class ResizeImage(BaseOperator):
    """图像缩放预处理
    """
    def __init__(self,
                 target_size=[32, 32],
                 by_short=False,
                 interpolation=cv2.INTER_LINEAR):
        super(ResizeImage, self).__init__("ResizeImage")
        self._target_size=target_size
        self._by_short=by_short
        self._interpolation=interpolation
    
    def _apply_image(self, sample):
        _img=sample['image']
        _img_shape=[]
        if self._by_short: # 按照图像实际短边与目标缩放的大小进行缩放
            _h, _w=_img.shape[:2]
            _min_hw=min(_h, _w) # 取短边
            _scaler=float(min(self.target_size)) / float(_min_hw) # 计算短边映射比例
            _h=int(_scaler*_h) # 修正宽高大小
            _w=int(_scaler*_w)
            _img=cv2.resize(_img, [_h, _w], interpolation=self._interpolation)
            _img_shape=[_h, _w, sample['image_shape'][-1]]
        else:
            _img=cv2.resize(_img, self._target_size, interpolation=self._interpolation)
        _img_shape=[self._target_size[0], self._target_size[1], sample['image_shape'][-1]]
        sample['image']=_img
        sample['image_shape']=_img_shape
        return sample

    def _apply_label(self, sample):
        _img=sample['label']
        _img_shape=[]
        if self._by_short: # 按照图像实际短边与目标缩放的大小进行缩放
            _h, _w=_img.shape[:2]
            _min_hw=min(_h, _w) # 取短边
            _scaler=float(min(self.target_size)) / float(_min_hw) # 计算短边映射比例
            _h=int(_scaler*_h) # 修正宽高大小
            _w=int(_scaler*_w)
            _img=cv2.resize(_img, [_h, _w], interpolation=self._interpolation)
            _img_shape=[_h, _w, sample['label_shape'][-1]]
        else:
            _img=cv2.resize(_img, self._target_size, interpolation=self._interpolation)
        _img_shape=[self._target_size[0], self._target_size[1], sample['label_shape'][-1]]
        sample['label']=_img
        sample['label_shape']=_img_shape
        return sample

@register
class FlipImage(BaseOperator):
    """图像翻转预处理
    """
    def __init__(self,
                 flip_mode=0):
        """
            flip_mode: 0-垂直翻转, 1-水平翻转, 2-水平+垂直同时翻转
        """
        super(FlipImage, self).__init__("FlipImage")
        if flip_mode not in [0, 1, -1]:
            logger.error(
                            "The flip_mode should choice in {0}, but not it is {1}.".format(
                            [0, 1, -1], flip_mode),
                            stack_info=True
                        )
            exit(1)
        self._flip_mode=flip_mode
    
    def _apply_image(self, sample):
        _img=sample['image']
        _img=cv2.flip(_img, flipCode=self._flip_mode)
        _h, _w=_img.shape[:2]
        sample['image']=_img
        sample['image_shape']=[_h, _w, sample['image_shape'][-1]]
        return sample

    def _apply_label(self, sample):
        _img=sample['label']
        _img=cv2.flip(_img, flipCode=self._flip_mode)
        _h, _w=_img.shape[:2]
        sample['label']=_img
        sample['label_shape']=[_h, _w, sample['label_shape'][-1]]
        return sample

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