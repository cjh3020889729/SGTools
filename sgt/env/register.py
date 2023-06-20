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
from typing import Any
from .logger import create_logger
logger=create_logger(log_name=__name__)

class SGTRegistry:
    """模块注册器
        register=SGTRegistry()

        @register()
        class XXXModule:
            def __init__(self):
                pass
    """
    def __init__(self, name='sgtools') -> None:
        """模块注册器初始化
            name: 注册器名称——默认为sgtools
        """
        self._name=name
        self._obj_map={}
    
    def __call__(self, obj) -> Any:
        """函数调用支持
            obj: 注册模块类
        """
        _name=obj.__name__
        if _name in self._obj_map.keys():
            logger.error("The Module({0}) is existed!".format(_name))
            exit(1)
        self._obj_map[_name]=obj

    def get(self, obj_name):
        """获取已注册模块
            obj_name: 模块名称
        """
        if obj_name not in self._obj_map.keys():
            logger.error("The Module({0}) isn't existed!".format(obj_name))
            exit(1)
        return self._obj_map[obj_name]
    
    def __len__(self):
        """获取已注册模块数量
        """
        return len(self._obj_map.keys())

# 构建注册器
register=SGTRegistry()
logger.info("Register Module is Loaded Successly!")