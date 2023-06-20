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
import numpy as np
from matplotlib import pyplot as plt
from typing import List

from ..env.logger import create_logger
from ..env.register import register
logger=create_logger(log_name=__name__)

@register
class SubgraphDrawing:
    def __init__(self,
                 graph_shape=[1, 1],
                 graph_fig_size=[12, 9]):
        self._check_graph_shape(graph_shape)
        self._graph_shape=graph_shape
        self._graph_fig_size=graph_fig_size
    
    def _check_graph_shape(self, graph_shape):
        if graph_shape[0] <= 0 or graph_shape[1] <= 0:
            logger.error(
                "The SubgraphDrawing only support the item of graph_shape({0}) >= 0.".format(graph_shape),
                stack_info=True
            )
            exit(1)

    def _check_targets_length(self, targets):
        if len(targets) != self._graph_shape[0]:
            logger.error(
                "The Subgraph Drawing Plot Meet | len(targets) != self._graph_shape[0] |, "
                "which only support the number of subgraph"
                " by self._graph_shape[0]({0} not {1}).".format(len(targets), self._graph_shape[0]),
                stack_info=True
            )
            exit(1)
    
    def _check_labels_length(self, labels):
        if len(labels) != self._graph_shape[0]:
            logger.error(
                "The Subgraph Drawing Plot Meet | len(labels) != self._graph_shape[0] |, "
                "which only support the number of subgraph"
                " by self._graph_shape[0]({0} not {1}).".format(len(labels), self._graph_shape[0]),
                stack_info=True
            )
            exit(1)
        for i in range(len(labels)):
            if len(labels[i]) != self._graph_shape[1]:
                logger.error(
                    "The Subgraph Drawing Plot Meet | len(labels[{0}]) != self._graph_shape[1] |, "
                    "which only support the number of subgraph"
                    " by self._graph_shape[1]({1} not {2}).".format(i, len(labels[i]), self._graph_shape[1]),
                    stack_info=True
                )
                exit(1)
    
    def _check_targets_valid(self, targets):
        self._check_targets_length(targets)
        _shape=targets[0].shape
        for _idx, _t in enumerate(targets):
            if _idx >= self._graph_shape[0]:
                break
            if _t.shape != _shape:
                logger.error(
                    "The SubgraphDrawing only support the shape of targets is equal.",
                    stack_info=True
                )
                exit(1)

    def _check_labels_valid(self, labels):
        self._check_labels_length(labels)
        for i in range(len(labels)):
            _shape=labels[i][0].shape
            for _idx, _t in enumerate(labels[i]):
                if _idx >= self._graph_shape[1]:
                    break
                if _t.shape != _shape:
                    logger.error(
                        "The SubgraphDrawing only support the shape of labels is equal.",
                        stack_info=True
                    )
                    exit(1)

    def plot(self,
             targets: List[np.ndarray],
             labels: List[List[np.ndarray]],
             titles: List[str]=None,
             save_path: str=None,
             plot_show: bool=False) -> None:
        """子图模式绘图接口
            targets: 绘制目标图像, 位于左子图
            labels: 绘制标签图像, 位于右子图
            titles: taget-label对的绘图标题
            save_path: 保存路径
        """
        self._check_targets_valid(targets=targets)
        self._check_labels_valid(labels=labels)
        plt.close()
        plt.figure(figsize=self._graph_fig_size)
        _title_sub_str=['target', 'label']
        for i in range(self._graph_shape[0]):
            for j in range(self._graph_shape[1]):
                _img= labels[i][j-1] if j > 0 else targets[i]
                _title=titles[i] if titles is not None else str(i)
                _title=_title + '-'
                _title=_title_sub_str[1] if j > 0 else _title_sub_str[0]
                plt.subplot(
                    i, j,
                    xlabel='{0}-{1}'.format(i+1, j+1),
                    title=_title
                )
                plt.imshow(_img)   
                plt.xticks([])
                plt.yticks([])
        if save_path != None:
            plt.imsave(fname=save_path)
        if plot_show:
            plt.show()




logger.info("Subgraph Drawing Plot Module is Loaded Successly!")