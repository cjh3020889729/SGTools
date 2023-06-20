# Scatter Generate Tool Environment

# logger简介
> 实现工具包的日志功能

- 支持指定日志器名称创建日志器
    - eg: create_logger(log_name=__name__) # __name__当前模块名称/文件名称
- 支持是否指定为根日志器创建来自动创建基于日期控制的日志器根目录
    - eg: `logs/2023_6_20_11_25_03`

# register简介
> 实现工具包的模块注册管理机制

