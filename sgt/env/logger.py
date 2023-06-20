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
import os, sys, time
import logging
import coloredlogs

__LOGGER_NAMES=[]
__LOG_DIR=None

def create_logger(log_name: str=None, log_dir: str='logs', is_root=False):
    """创建日志记录器
        log_name: 日志名称——若为None, 则为当前日志创建日期
        log_dir: 日志保存目录
        is_root: 是否为根日志创建——是则创建对应的日志目录与文件，否则只是创建日志器
    """
    global __LOGGER_NAMES, __LOG_DIR
    log_file="log.txt"
    log_dir=os.path.join(log_dir, str(time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime())))
    if is_root: # 检查是否为根日志创建
        __LOG_DIR=log_dir
    else:
        log_dir=__LOG_DIR
    if log_dir is not None and not os.path.exists(log_dir):
        os.makedirs(log_dir) # 创建期望保存日志的目录
    if log_name is None: # 未指定日志名时，自动填充日期作为日志名
        log_name=str(time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()))
    if log_name in __LOGGER_NAMES:
        logger = logging.getLogger(log_name) # 若已存在该日志器，则直接返回
        return logger
    # 创建日志器
    logger = logging.getLogger(log_name)
    logger.handlers.clear() # 初始化日志处理器空间
    logger.setLevel(logging.DEBUG) # 设置日志器日志级别

    # 构建日志信息的文件流处理器
    handler_file = logging.FileHandler(os.path.join(__LOG_DIR, log_file), mode='a')
    handler_file.setLevel(logging.DEBUG)
    handler_file.setFormatter(
        logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt="%m/%d/%Y %H:%M:%S %p"
        )
    )

    # 构建日志信息的流处理器
    handler_stdout = logging.StreamHandler(sys.stdout)
    handler_stdout.setLevel(logging.DEBUG)
    handler_stdout.setFormatter( # 标准输出如果允许的情况下自动支持颜色显示
        coloredlogs.ColoredFormatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s: %(message)s', datefmt="%Y-%m-%d %H:%M:%S %p",
            level_styles=dict(
                debug=dict(color='white'),
                info=dict(color='green'),
                warning=dict(color='yellow', bright=True),
                error=dict(color='red', bold=True, bright=True),
                critical=dict(color='black', bold=True, background='red'),
            )
        )
    )

    # 日志器加入创建的日志处理器
    logger.addHandler(handler_file)
    logger.addHandler(handler_stdout)
    return logger

# 创建根日志
logger=create_logger(log_name=__name__, is_root=True)
logger.info("Logging Module is Loaded Successly!")