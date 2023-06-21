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
    """子图对照可视化
    """
    def __init__(self,
                 graph_shape: List[int]=[1, 1],
                 graph_fig_size: List[int]=[12, 9]):
        """
            graph_shape: 可视化对照图排布——[原始图数量, 每张原始图的对照图数量+1]
            graph_fig_size: 可视化绘图画板大小
        """
        self._check_graph_shape(graph_shape)
        self._graph_shape=graph_shape
        self._graph_fig_size=graph_fig_size
    
    def _check_graph_shape(self, graph_shape: List[int]) -> None:
        """检查绘图排版有效性
            graph_shape: 可视化对照图排布——[原始图数量, 每张原始图的对照图数量+1]
        """
        if graph_shape[0] <= 0 or graph_shape[1] <= 0:
            logger.error(
                "The SubgraphDrawing only support the item of graph_shape({0}) >= 0.".format(graph_shape),
                stack_info=True
            )
            exit(1)

    def _check_images_length(self, images: List[np.ndarray]) -> None:
        """检查绘图时原始图数量是否与排版一致
            images: 原始图数据组成的列表
        """
        if len(images) != self._graph_shape[0]:
            logger.error(
                "The Subgraph Drawing Plot Meet | len(images) != self._graph_shape[0] |, "
                "which only support the number of subgraph"
                " by self._graph_shape[0]({0} not {1}).".format(len(images), self._graph_shape[0]),
                stack_info=True
            )
            exit(1)
    
    def _check_labels_length(self, labels: List[List[np.ndarray]]) -> None:
        """检查绘图时原始图的对照图数量是否与排版一致
            labels: 每组对照图数据组成的列表
        """
        if len(labels) != self._graph_shape[0]:
            logger.error(
                "The Subgraph Drawing Plot Meet | len(labels) != self._graph_shape[0] |, "
                "which only support the number of subgraph"
                " by self._graph_shape[0]({0} not {1}).".format(len(labels), self._graph_shape[0]),
                stack_info=True
            )
            exit(1)
        for i in range(len(labels)):
            if len(labels[i]) != (self._graph_shape[1]-1):
                logger.error(
                    "The Subgraph Drawing Plot Meet | len(labels[{0}]) != self._graph_shape[1] |, "
                    "which only support the number of subgraph"
                    " by self._graph_shape[1]({1} not {2}).".format(i, len(labels[i]), self._graph_shape[1]),
                    stack_info=True
                )
                exit(1)
    
    def _check_images_valid(self, images: List[np.ndarray]) -> None:
        """检查绘图时原始图有效性
            images: 原始图数据组成的列表
        """
        self._check_images_length(images)
        _shape=images[0].shape
        for _idx, _t in enumerate(images):
            if _idx >= self._graph_shape[0]:
                break
            if _t.shape != _shape:
                logger.error(
                    "The SubgraphDrawing only support the shape of images is equal.",
                    stack_info=True
                )
                exit(1)

    def _check_labels_valid(self, labels: List[List[np.ndarray]]) -> None:
        """检查绘图时原始图的对照图有效性
            labels: 每组对照图数据组成的列表
        """
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
             images: List[np.ndarray],
             labels: List[List[np.ndarray]],
             titles: List[str]=None,
             save_path: str=None,
             plot_show: bool=False) -> None:
        """子图模式绘图接口
            images: 绘制原始图像, 位于左子图
            labels: 绘制标签图像, 位于右子图
            titles: taget-label对的绘图标题
            save_path: 保存路径
            plot_show: 是否及时显示
        """
        self._check_images_valid(images=images)
        self._check_labels_valid(labels=labels)
        plt.close()
        plt.figure(figsize=self._graph_fig_size)
        _title_sub_str=['target', 'label']
        for i in range(self._graph_shape[0]):
            for j in range(self._graph_shape[1]):
                _img= labels[i][j-1] if j > 0 else images[i]
                _title=titles[i] if titles is not None else str(i)
                _title+='-'
                _title+=_title_sub_str[1] if j > 0 else _title_sub_str[0]
                plt.subplot(self._graph_shape[0], self._graph_shape[1], i*self._graph_shape[1]+j+1)
                plt.imshow(_img)   
                plt.title(_title)
                plt.xlabel('{0}-{1}'.format(i+1, j+1))
                plt.xticks([])
                plt.yticks([])
        plt.subplots_adjust(bottom=0.05, top=0.95, wspace=0.5, hspace=0.5)
        if save_path != None:
            if not os.path.exists(os.path.dirname(save_path)):
                logger.warning("The save_path_dir({0}) of Subgraph Drawing Plot is not exists"
                               ", so it will be auto created.".format(os.path.dirname(save_path)))
                os.makedirs(os.path.dirname(save_path))
            plt.savefig(save_path)
        if plot_show:
            plt.show()

logger.info("Subgraph Drawing Plot Module is Loaded Successly!")