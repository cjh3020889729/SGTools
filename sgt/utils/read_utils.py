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
import cv2
from typing import List

from ..env.logger import create_logger
logger=create_logger(log_name=__name__)

def read_dir_images(img_dir: str) -> List[str]:
    """读取一个目录下的所有图片路径
        img_dir: 图片目录
    """
    if not os.path.exists(img_dir):
        logger.error("The Image Dir is not existed!", stack_info=True)
        exit(1)
    _img_files=[]
    for _, _, files in os.walk(img_dir):
        sorted(files)
        for _f in files:
            if _f.split('.')[-1] in ['jpg', 'bmp', 'png', 'jpeg']:
                _img_files.append(os.path.join(img_dir, _f))
    if len(_img_files) == 0:
        logger.warning("The Image Dir is empty!")
    else:
        logger.info("The Image Dir has read {0} images!".format(len(_img_files)))
    return _img_files
