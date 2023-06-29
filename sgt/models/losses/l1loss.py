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
from paddle import nn

from ...env.register import register
from ...env.logger import create_logger
logger=create_logger(log_name=__name__)

__all__=[
    'L1Loss'
]

@register
class L1Loss(nn.Layer):
    """L1绝对值损失
    """
    def __init__(self,
                 reduction='mean',
                 weights=None):
        """
            reduction: 聚合模式——'mean', 'sum'
            weights: 损失分通道计算权重——如果为None, 则等价于默认计算;
                     如果为list, 则分别对应每一个通道上计算损失时的权重。
        """
        super(L1Loss, self).__init__()
        self._check_reduction(reduction)
        self.weights=self._check_weights(weights)
        self._loss_func=nn.L1Loss(reduction=reduction)
    
    def forward(self, preds, targets):
        self._check_shape(preds.detach(), targets.detach())

        _loss=None
        if self.weights != None:
            if len(targets.shape) == 3 and len(self.weights) == 1: 
                _loss=self._loss_func(preds, targets)
            elif len(targets.shape) == 4 and len(self.weights) == targets.shape[-1]:
                for _idx, w in enumerate(self.weights):
                    if _loss != None:
                        _loss += w * self._loss_func(preds[:, :, :, _idx], targets[:, :, :, _idx])
                    else:
                        _loss = w * self._loss_func(preds[:, :, :, _idx], targets[:, :, :, _idx])
        else:
            _loss=self._loss_func(preds, targets)

        return {
            'loss': _loss
        }

    def _check_reduction(self, reduction):
        """检查聚合模式
        """
        if reduction not in ['mean', 'sum']:
            logger.error("The L1Loss Only Support The Mode Of 'mean' And 'sum'.",
                         stack_info=True)
            exit(1)

    def _check_weights(self, weights):
        """检查权重比例的有效性
        """
        if weights != None and isinstance(weights, list):
            logger.warning("The L1Loss weights only support None or list.")
            return None
        return weights

    def _check_shape(self, preds, targets):
        """检查预测与目标的shape是否一致
        """
        if preds.shape != targets.shape:
            logger.error("The L1Loss need the preds.shape == targets.shape.",
                         stack_info=True)
            exit(1)
