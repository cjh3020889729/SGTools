# Scatter Generate Tool Transforms

-----------

# transforms简介
> 实现常见的单样本预处理方法

## 1.主要内容
- 支持图像预处理组合
```python
transfroms=Compose(
                        [
                            EncodeImage(),
                            FlipImage(),
                            Normalize()
                        ]
                    )
sample=transforms(sample)
```
- 支持图像读取
```python
transform=EncodeImage()
sample=transform(sample) # add image + label data
```
- 支持图像缩放
```python
transform=ResizeImage()
sample=transform(sample) # resize image + label
```
- 支持图像翻转
```python
transform=FlipImage()
sample=transform(sample) # flip image + label
```
- 支持图像归一化
```python
transform=Normalize()
sample=transform(sample) # normalize image + label
```
- 随机系列待支持...

-----------

# batch_transforms简介
> 实现常见的批量样本预处理方法

## 1.主要内容
- 支持批样本提取——只要用于数据集加载时批样本采样
```python
transforms=BatchCompose([])
samples=transforms(samples) # 将样本按key聚合起来: {'image': [], ...}
```
- 待支持...

-----------

# ops简介
> 提供常见预处理的子方法

## 1.主要内容
- 待支持...