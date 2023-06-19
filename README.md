# SGTools
> SGTools: Scatter Generate Tools

## 介绍

这是一个基于PaddlePaddle的散射成像调控深度学习训练工具，包括用于图像生成深度学习模型的训练、评估与可视化；同时也支持自定义模型以及其它组件。

-----------

## 项目结构

```txt
|--configs: 训练用配置文件
|--docs: 工具详细文档
|--examples: 工具使用示例
|--tools: 工具常用方法
|--sgt: 工具源代码
    |--env: 工具环境相关: eg: logger
    |--utils: 不可或缺但不属于关键的操作
    |--transforms: 数据输入前的预处理
    |--models: 模型库
        |--encoders: 包含多种编码器部分的模型实现
        |--decoders: 包含多种解码器部分的模型实现
        |--archs: 包含模型组织架构的实现
        |--losses: 包含模型训练损失的实现
    |--metrics: 评价指标
    |--summarys: 分析/统计输入/输出数据的接口
    |--visualizes: 可视化接口

```

-----------

## 示例
> 其它示例参考: `examples`目录

-----------

## 文档

    详情参考: `docs`目录

-----------

## 引用说明

