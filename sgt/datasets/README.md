# Scatter Generate Tool datasets

-----------

# base简介
> 实现基本的数据集基类与数据加载器

## 1.主要内容
- 实现数据集训练与评估的基类
- 实现测试数据集
- 实现数据集加载器的基类
- 实现训练、评估、测试的数据集加载器

## 2.主要接口
- TestDataset
```python
class TestDataset(Dataset):
    def __init__(self,
                 image_dir: str):
        super(TestDataset, self).__init__()
```
- TrainDataLoader
```python
class TrainDataLoader(BaseDataLoader):
    """训练数据加载器
    """
    def __init__(self,
                 dataset: Dataset,
                 sample_transforms: List[Any] = [],
                 batch_transforms: List[Any] = [],
                 batch_size: int = 1,
                 shuffle: bool = True,
                 drop_last: bool = False,
                 worker_num: int = 1):
        super(TrainDataLoader, self).__init__(
                                                dataset,
                                                sample_transforms,
                                                batch_transforms,
                                                batch_size,
                                                shuffle,
                                                drop_last,
                                                worker_num
                                            )
```
- EvalDataLoader
```python
class EvalDataLoader(BaseDataLoader):
    """验证数据加载器
    """
    def __init__(self,
                 dataset: Dataset,
                 sample_transforms: List[Any] = [],
                 batch_transforms: List[Any] = [],
                 batch_size: int = 1,
                 worker_num: int = 1):
        super(EvalDataLoader, self).__init__(
                                                dataset,
                                                sample_transforms,
                                                batch_transforms,
                                                batch_size,
                                                False,
                                                False,
                                                worker_num
                                            )
```
- TestDataLoader
```python
class TestDataLoader(BaseDataLoader):
    """测试数据加载器
    """
    def __init__(self,
                 dataset: Dataset,
                 sample_transforms: List[Any] = [],
                 batch_transforms: List[Any] = [],
                 batch_size: int = 1,
                 worker_num: int = 1):
        super(TestDataLoader, self).__init__(
                                                dataset,
                                                sample_transforms,
                                                batch_transforms,
                                                batch_size,
                                                False,
                                                False,
                                                worker_num
                                            )
```

-----------

# normal简介
> 实现一种通用基础的数据集类

## 1.主要内容
- 实现Normal训练数据集类
- 实现Normal评估数据集类

## 2.主要接口
- TrainNormalDataset
```python
class TrainNormalDataset(NormalDataset):
    def __init__(self,
                 data_dir: str,
                 data_txt: str):
        super(TrainNormalDataset, self).__init__(
                            data_dir,
                            data_txt,
                            True
                        )
```
- EvalNormalDataset
```python
class EvalNormalDataset(NormalDataset):
    def __init__(self,
                 data_dir: str,
                 data_txt: str):
        super(TrainNormalDataset, self).__init__(
                            data_dir,
                            data_txt,
                            False
                        )
```
