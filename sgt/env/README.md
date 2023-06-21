# Scatter Generate Tool Environment

-----------

# logger简介
> 实现工具包的日志功能

## 1.主要内容
- 支持指定日志器名称创建日志器
    - eg: create_logger(log_name=__name__) # __name__当前模块名称/文件名称
- 支持是否指定为根日志器创建来自动创建基于日期控制的日志器根目录
    - eg: `logs/2023_6_20_11_25_03`

## 2.核心参数
- `__LOGGER_NAMES`: 所有已有日志记录器的名称缓存，用于判别是否为已创建的日志器
- `__LOG_DIR`: 根目录日志器日志缓存所在目录，用于统一日志器缓存路径

-----------

# register简介
> 实现工具包的模块注册管理机制

## 1.主要内容
- 支持注册已有的类与函数
```python
@register
class TestModule:
    ...
```
- 允许基于注册机制的调用
```python
register.get('TestModule') # 等价于直接使用TestModule
```
- 允许查询已注册模块数量
```python
len(register)
```
- 允许导出已注册模块名称
```python
register.export_module_list()
```

-----------

# vdlrecords简介-TODO
> 实现基于visualdl的可视化日志记录: 包括标量数据、图像数据以及参数数据。

## 1.主要内容
- 支持标量数据记录与可视化
- 支持图像数据记录与可视化
- 支持参数数据记录与可视化
