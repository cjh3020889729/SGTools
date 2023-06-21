import cv2

from sgt.env.logger import create_logger
from sgt.transforms import transforms, batch_transforms
from sgt.visualizes.subs_plot import SubgraphDrawing
from sgt.env.register import register

from sgt.utils.read_utils import read_dir_images

from sgt.datasets.base import TestDataset, TrainDataLoader
from sgt.datasets.normal import TrainNormalDataset


logger = create_logger(log_name=__name__)
logger.info("Test Module is Loaded!")

# 测试Test数据集
# test_dataset=TestDataset(
#     image_dir='datasets/normal/images')
# test_dataset.parse_dataset()
# print(test_dataset[0])

# 测试Normal数据集
# train_normal_dataset=TrainNormalDataset(
#     data_dir='datasets/normal',
#     data_txt='train.txt')
# train_normal_dataset.parse_dataset()
# print(train_normal_dataset[0])

# 测试基于Normal的数据加载器
# train_normal_dataset=TrainNormalDataset(
#     data_dir='datasets/normal',
#     data_txt='train.txt')
# train_normal_dataloader=TrainDataLoader(
#     dataset=train_normal_dataset,
#     sample_transforms=[transforms.EncodeImage(), transforms.Normalize()],
#     batch_transforms=[],
#     batch_size=2,
#     shuffle=True,
#     drop_last=False,
#     worker_num=0
# )
# for batch in train_normal_dataloader:
#     print(batch)
#     break

# 测试注册器
# subs_plot=register.get('SubgraphDrawing')(
#     graph_shape=[1, 1],
#     graph_fig_size=[12, 9]
# )

# 测试对照绘图
# images_img_path=read_dir_images(img_dir='datasets/normal/images')[:5]
# labels_img_path=read_dir_images(img_dir='datasets/normal/labels')[:5]

# images_img=[cv2.cvtColor(cv2.imread(i), cv2.COLOR_BGR2RGB) for i in images_img_path]
# labels_img=[[cv2.cvtColor(cv2.imread(i), cv2.COLOR_BGR2RGB)] for i in labels_img_path]

# subs_plot=SubgraphDrawing(
#     graph_shape=[len(images_img), len(labels_img[0])+1],
#     graph_fig_size=[12, 9]
# )

# subs_plot.plot(
#     images=images_img,
#     labels=labels_img,
#     titles=None,
#     save_path='outputs/visual_imgs/subs_plot.png',
#     plot_show=False
# )

