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

from ..env.logger import create_logger
from ..env.register import register
from ..transforms.transforms import Compose
from ..transforms.batch_transforms import BatchCompose
from ..utils.read_utils import read_dir_images
logger=create_logger(log_name=__name__)

from paddle.io import Dataset, DataLoader, DistributedBatchSampler


class BaseDataset(Dataset):
    def __init__(self,
                 data_dir: str,
                 data_txt: str,
                 is_train_or_eval: bool=True):
        super(BaseDataset, self).__init__()
        self._data_dir=data_dir
        self._data_txt=data_txt
        self._is_train_or_eval=is_train_or_eval

        self._transforms=None

    def parse_dataset(self) -> None:
        """解析data_txt添加样本图像path列表
        """
        NotImplementedError("The Dataset Must Need To Implement The `parse_dataset` function!")
    
    def set_sample_transforms(self, transforms: List[Any]) -> None:
        """设置采样预处理方法
        """
        self._transforms=transforms
    
    def __getitem__(self, idx: int) -> None:
        """采样一个样本
            {
                'image_path':
                'label_path':
                'image':
                'image_shape':
                'label':
                'label_shape':
            }
        """
        sample={}
        sample['image_path']=self._images[idx]
        sample['label_path']=self._labels[idx]
        if self._transforms is not None:
            sample=self._transforms(sample)
        return sample

    def __len__(self) -> int:
        return len(self._images)

@register
class TestDataset(Dataset):
    def __init__(self,
                 image_dir: str):
        super(TestDataset, self).__init__()
        self._image_dir=image_dir

        self._transforms=None

    def parse_dataset(self) -> None:
        """解析image_dir中的图片添加到path列表
        """
        if not os.path.exists(self._image_dir):
            logger.error(
                "The TestDataset image_dir({0}) is not exists!".format(self._image_dir),
                stack_info=True
            )
            exit(1)
        _start_time=time()
        logger.info("The TestDataset Has Load image_dir: {0}.".format(self._image_dir))
        _images=read_dir_images(self._image_dir)
        self._images=_images
        self._labels=None
        logger.info("The TestDataset Has Collect Image samples: {0}.".format(len(_images)))
        logger.info("The TestDataset Load Data Cost Time: {0} s.".format(time()-_start_time))
    
    def set_sample_transforms(self, transforms: List[Any]) -> None:
        """设置采样预处理方法
        """
        self._transforms=transforms
    
    def __getitem__(self, idx:int) -> None:
        """采样一个样本
            {
                'image_path':
                'label_path':
                'image':
                'image_shape':
                'label':
                'label_shape':
            }
        """
        sample={}
        sample['image_path']=self._images[idx]
        sample['label_path']=self._images[idx] # test data hasn't labels
        if self._transforms is not None:
            sample=self._transforms(sample)
        return sample

    def __len__(self) -> int:
        return len(self._images)

class BaseDataLoader:
    """基础数据加载器
    """
    def __init__(self,
                 dataset: Dataset,
                 sample_transforms: List[Any]=[],
                 batch_transforms: List[Any]=[],
                 batch_size: int=32,
                 shuffle: bool=False,
                 drop_last: bool=False,
                 worker_num: int=0):
        self._sample_transforms=Compose(sample_transforms)
        self._batch_transforms=BatchCompose(batch_transforms)
        self._batch_size=batch_size
        self._shuffle=shuffle
        self._drop_last=drop_last
        self._worker_num=worker_num

        self._dataset=dataset
        self._dataset.parse_dataset()
        self._dataset.set_sample_transforms(self._sample_transforms)

        self._batch_sampler = DistributedBatchSampler(
                                    self._dataset,
                                    batch_size=self._batch_size,
                                    shuffle=self._shuffle,
                                    drop_last=self._drop_last)
        self._dataloader = DataLoader(
            dataset=self._dataset,
            batch_sampler=self._batch_sampler,
            collate_fn=self._batch_transforms,
            num_workers=worker_num)
        self._loader = iter(self._dataloader)
    
    def __len__(self) -> int:
        """每轮训练迭代次数
        """
        return len(self._batch_sampler)
    
    def __iter__(self):
        """返回迭代本身
        """
        return self
    
    def __next__(self):
        """迭代下一个元素
        """
        try:
            return next(self._loader)
        except StopIteration:
            self._loader = iter(self._dataloader)
            six.reraise(*sys.exc_info())

@register
class TrainDataLoader(BaseDataLoader):
    """训练数据加载器
    """
    def __init__(self,
                 dataset: Dataset,
                 sample_transforms: List[Any] = [],
                 batch_transforms: List[Any] = [],
                 batch_size: int = 1,
                 shuffle: bool = True,
                 drop_last: bool = False,
                 worker_num: int = 1):
        super(TrainDataLoader, self).__init__(
                                                dataset,
                                                sample_transforms,
                                                batch_transforms,
                                                batch_size,
                                                shuffle,
                                                drop_last,
                                                worker_num
                                            )

@register
class EvalDataLoader(BaseDataLoader):
    """验证数据加载器
    """
    def __init__(self,
                 dataset: Dataset,
                 sample_transforms: List[Any] = [],
                 batch_transforms: List[Any] = [],
                 batch_size: int = 1,
                 worker_num: int = 1):
        super(EvalDataLoader, self).__init__(
                                                dataset,
                                                sample_transforms,
                                                batch_transforms,
                                                batch_size,
                                                False,
                                                False,
                                                worker_num
                                            )

@register
class TestDataLoader(BaseDataLoader):
    """测试数据加载器
    """
    def __init__(self,
                 dataset: Dataset,
                 sample_transforms: List[Any] = [],
                 batch_transforms: List[Any] = [],
                 batch_size: int = 1,
                 worker_num: int = 1):
        super(TestDataLoader, self).__init__(
                                                dataset,
                                                sample_transforms,
                                                batch_transforms,
                                                batch_size,
                                                False,
                                                False,
                                                worker_num
                                            )

logger.info("DataLoader Module is Loaded Successly!")