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
from copy import deepcopy

import paddle
from paddle import nn

from ..env.register import register
from ..env.logger import create_logger
logger=create_logger(log_name=__name__)

__all__=[
    'SegTrainer'
]

from ..models import *
from ..datasets import *
from ..metrics import *
from ..summarys import *
from ..utils import *
from ..transforms import *
from ..visualizes import *

class SegTrainer:
    """基于分割的训练器
    """
    def __init__(self,
                 config,
                 mode='train'):
        """
        """
        self.cfg=deepcopy(config)
        self.mode=mode.lower()
    
    def _init_model(self):
        """初始化模型
        """
    
    def _init_opt(self):
        """初始化优化器
        """
    
    def _init_loss(self):
        """初始化损失
        """
    
    def _init_metrics(self):
        """初始化评价指标
        """
    
    def _reset_metrics(self):
        """重置评价指标数据
        """
    
    def _load_weights(self):
        """加载权重
        """
    
    def _save_weights(self):
        """保存权重
        """
    
    def _resume_weights(self):
        """断续加载权重
        """
    
    def _init_dataloader(self):
        """初始化数据加载器
        """
    
    def _init_visualize(self):
        """初始化可视化方法
        """

    def train(self):
        """训练接口
        """
    
    def eval(self):
        """评估接口
        """
    
    def predict(self):
        """预测接口
        """
    
    def _flops(self):
        """计算运算量
        """


    




