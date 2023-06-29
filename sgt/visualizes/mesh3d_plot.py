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
import pyvista as pv
from pyvista import themes
from matplotlib import pyplot as plt
from typing import List, Any

from ..env.logger import create_logger
from ..env.register import register
logger=create_logger(log_name=__name__)

__all__=[
    'Mesh3DDrawing'
]

@register
class Mesh3DDrawing:
    """三维Mesh偏差可视化
    """
    def __init__(self):
        """
        """
    
    def _check_inputs(self,
                      image: np.ndarray,
                      label: np.ndarray) -> None:
        """检查可视化输入是否有效——shape一致化
            image: 输入原图
            label: 输入目标图
        """
        if image.shape != label.shape:
            logger.error(
                "The Mesh3D Drawing Only Support The Same Shape of (image, label),"
                "but now image is {0}, label is {1}.".format(image.shape, label.shape),
                stack_info=True
            )
            exit(1)
    
    def _normalize(self, img: np.ndarray) -> np.ndarray:
        """缩放图像数据到0-1之间
        """
        img=img.astype('float32')/255.
        return img
    
    def _find_channel_num(self, img: np.ndarray) -> int:
        """查询输入图像的通道数
        """
        if len(img.shape) == 2:
            return 1
        elif len(img.shape) == 3:
            return 3
        else:
            return -1
    
    def plot(self,
             image: Any,
             label: Any,
             save_path: str=None,
             plot_show: bool=True) -> None:
        if save_path != None: # 自动切换是否及时显示——只允许不保存时及时显示
            plot_show=False
        # 检查参数
        self._check_inputs(image, label)
        image=self._normalize(image)
        label=self._normalize(label)
        _num_channels=self._find_channel_num(image)
        pv.set_plot_theme(themes.DocumentTheme())
        # 设置映射网格坐标
        x = np.arange(0, image.shape[1], 1)
        y = np.arange(0, image.shape[0], 1)
        x, y = np.meshgrid(x, y)
        if _num_channels==1: # 灰度图制偏差Mesh对照图
            pv.global_theme.multi_rendering_splitting_position = 0.50
            plotter = pv.Plotter(shape='2|1', off_screen= False if plot_show else True)

            # 绘制image
            plotter.subplot(0)
            plotter.add_text("Origin Image", font_size=10)
            _sub_data=np.concatenate([image.reshape(image.shape[0], image.shape[1], 1)]*3, axis=-1)
            fig=plt.figure() # 引入matplotlib绘制图像
            plt.imshow(_sub_data)
            chart = pv.ChartMPL(fig)
            plotter.add_chart(chart)

            # 绘制label
            plotter.subplot(1)
            plotter.add_text("Origin Label", font_size=10)
            _sub_data=np.concatenate([label.reshape(label.shape[0], label.shape[1], 1)]*3, axis=-1)
            fig=plt.figure() # 引入matplotlib绘制图像
            plt.imshow(_sub_data)
            chart = pv.ChartMPL(fig)
            plotter.add_chart(chart)

            # 绘制偏差Mesh图
            plotter.subplot(2)
            plotter.add_text("Deviation Mesh", font_size=10)
            _sub_data=image-label # 计算差值
            grid = pv.StructuredGrid(x, y, _sub_data)
            grid["Error"] = _sub_data.ravel(order="F")
            plotter.add_mesh(grid.outline(), color='black') # 绘制最小外边界
            plotter.add_mesh(grid,
                             show_edges=True,
                             show_scalar_bar=False,
                             smooth_shading=True,
                             split_sharp_edges=True,
                             point_size=1) # 绘制三维网格图像
            plotter.add_floor('-z', opacity=0.6, show_edges=True, offset=0.2) # 添加背景板
            plotter.add_scalar_bar(
                'Error',
                vertical=False,
                outline=False,
                title_font_size=12,
                label_font_size=12,
                fmt='%{0}.2f'.format(int(np.abs(_sub_data).max())),
            ) # 添加标量条
            plotter.show_bounds(font_size=8)
            plotter.show_axes()

            if save_path != None:
                if not os.path.exists(os.path.dirname(save_path)):
                    logger.warning("The save_path_dir({0}) of Mesh3D Drawing Plot is not exists"
                                ", so it will be auto created.".format(os.path.dirname(save_path)))
                    os.makedirs(os.path.dirname(save_path))
                plotter.screenshot(save_path)
            if plot_show:
                plotter.show()
        elif _num_channels==3: # RGB图制偏差Mesh对照图
            pv.global_theme.multi_rendering_splitting_position = 0.60
            plotter = pv.Plotter(shape='2|3', off_screen= False if plot_show else True)

            # 绘制image
            plotter.subplot(0)
            plotter.add_text("Origin Image", font_size=10)
            _sub_data=image
            fig=plt.figure() # 引入matplotlib绘制图像
            plt.imshow(_sub_data)
            chart = pv.ChartMPL(fig)
            plotter.add_chart(chart)

            # 绘制label
            plotter.subplot(1)
            plotter.add_text("Origin Label", font_size=10)
            _sub_data=label
            fig=plt.figure() # 引入matplotlib绘制图像
            plt.imshow(_sub_data)
            chart = pv.ChartMPL(fig)
            plotter.add_chart(chart)

            # 通道1: 绘制偏差Mesh图
            _sub_datas=image-label
            plotter.subplot(2)
            plotter.add_text("Channel1:Deviation Mesh", font_size=10)
            _sub_data=_sub_datas[:, :, 0]
            grid = pv.StructuredGrid(x, y, _sub_data)
            grid["Error"] = _sub_data.ravel(order="F")
            plotter.add_mesh(grid.outline(), color='black')
            plotter.add_mesh(grid,
                             show_edges=True,
                             show_scalar_bar=False,
                             smooth_shading=True,
                             split_sharp_edges=True,
                             point_size=1)
            plotter.add_floor('-z', opacity=0.6, show_edges=True, offset=0.2)
            plotter.show_bounds(font_size=8)

            # 通道2: 绘制偏差Mesh图
            plotter.subplot(3)
            plotter.add_text("Channel2:Deviation Mesh", font_size=10)
            _sub_data=_sub_datas[:, :, 1]
            grid = pv.StructuredGrid(x, y, _sub_data)
            grid["Error"] = _sub_data.ravel(order="F")
            plotter.add_mesh(grid.outline(), color='black')
            plotter.add_mesh(grid,
                             show_edges=True,
                             show_scalar_bar=False,
                             smooth_shading=True,
                             split_sharp_edges=True,
                             point_size=1)
            plotter.add_floor('-z', opacity=0.6, show_edges=True, offset=0.2)
            plotter.show_bounds(font_size=8)

            # 通道3: 绘制偏差Mesh图
            plotter.subplot(4)
            plotter.add_text("Channel3:Deviation Mesh", font_size=10)
            _sub_data=_sub_datas[:, :, 2]
            grid = pv.StructuredGrid(x, y, _sub_data)
            grid["Error"] = _sub_data.ravel(order="F")
            plotter.add_mesh(grid.outline(), color='black')
            plotter.add_mesh(grid,
                             show_edges=True,
                             show_scalar_bar=False,
                             smooth_shading=True,
                             split_sharp_edges=True,
                             point_size=1)
            plotter.add_floor('-z', opacity=0.6, show_edges=True, offset=0.2)
            plotter.add_scalar_bar(
                    'Error',
                    vertical=True,
                    outline=False,
                    title_font_size=12,
                    label_font_size=12,
                    fmt='%{0}.2f'.format(int(np.abs(_sub_data).max())),
                )
            plotter.show_bounds(font_size=8)

            if save_path != None:
                if not os.path.exists(os.path.dirname(save_path)):
                    logger.warning("The save_path_dir({0}) of Mesh3D Drawing Plot is not exists"
                                ", so it will be auto created.".format(os.path.dirname(save_path)))
                    os.makedirs(os.path.dirname(save_path))
                plotter.screenshot(save_path)
            if plot_show:
                plotter.show()
        else:
            logger.error(
                "The Mesh3D Drawing Only Support The number of image channel is 1 or 3.",
                stack_info=True
            )
            exit(1)

logger.info("Mesh3D Drawing Plot Module is Loaded Successly!")