"""
This dataset is designed to verify the efficiency of pointcnn

该文件包含了用于验证PointCNN效率的数据集实现。主要内容如下:

1. gen4l_collate_fn: 用于批处理数据的函数
2. test_collate_fn: 用于测试数据的批处理函数
3. Gen4L9MeterDataset: 主要的数据集类,用于加载和处理图像和标签数据

数据集特点:
- 支持训练和测试两种模式
- 图像大小为32x300像素
- 标签长度为9位数字, 其中有效位数为7位。
- 支持随机位置查询和one-hot编码

该数据集设计用于PointCNN模型的训练和评估,可以生成图像、位置查询和对应标签的样本。

created_at: 09/09/2024
author: svtter

"""

# from collections import namedtuple
import pathlib
import random
import typing as t

import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset

# from cnn_lstm_ctc.usetorch.shared import transforms
# from meterfuncs.dataset import use_embed


def gen4l_collate_fn(batch):
  # image, pos, pos_tensor, label[pos], length
  images, pos, pos_tensors, labels, full_labels, lengths = zip(*batch)

  images = torch.stack(images, 0)  # images: tuple[tensor]
  labels = torch.stack(labels, 0)
  pos_tensors = torch.stack(pos_tensors, 0)
  # [batch_size, width, height, channel]
  # [batch_size, 74]
  # [batch_size, 1]

  # return images, pos_tensors, labels, full_labels, lengths
  return images, pos_tensors, labels


def test_collate_fn(batch):
  images, pos, pos_tensors, labels, full_labels, lengths = zip(*batch)

  images = torch.stack(images, 0)  # images: tuple[tensor]
  labels = torch.stack(labels, 0)
  pos_tensors = torch.stack(pos_tensors, 0)

  batch_data = (images, pos_tensors, labels, full_labels, lengths)
  return batch_data[:3]


class Gen4L9MeterDataset(Dataset):
  """4w dataset, 9 digits label. This dataset is construct to img, query, label. To get more details, read the __get_item__ source code.
  load label from np file, the label `1` mapping to `1`.
  The data shape is [1, 32, 300], the label shape is [11], the pos shape is [10].
  """

  def __init__(
    self,
    root_dir: t.Union[pathlib.Path, str],
    mode: t.Literal["test", "train"],
    limit: bool = False,
    transforms=None,
  ):
    # h, w = (37, 297)
    if mode == "train":
      x_name = "x_train.npy"
      y_name = "y_train.npy"
    elif mode == "test":
      x_name = "x_test.npy"
      y_name = "y_test.npy"

    x_path = pathlib.Path(root_dir) / x_name
    y_path = pathlib.Path(root_dir) / y_name
    self.limit = limit
    self.imgs = np.load(x_path)
    self.trans_f = transforms.get_meter_transforms()
    self.imgs = self.trans_f(self.imgs)
    self.imgs = torch.FloatTensor(self.imgs)
    self.imgs = self.imgs / 255.0

    self.labels = np.load(y_path)

  def load_from_np(self, y_path):
    self.labels = np.load(y_path)
    self.labels = torch.LongTensor(self.labels)

  def __len__(self):
    return self.imgs.shape[0]

  def use_limit_range(self, length, label):
    # 随机给一个位置以及一个 query 向量, pos_tensor 中可以有没有用到的数据
    pos = random.randrange(0, 7)
    pos_tensor = F.one_hot(torch.tensor(pos), num_classes=10).float()

    # 0-9 map to 0-9, x map to 10
    single_label = F.one_hot(label[pos], num_classes=11).float()

    return pos, pos_tensor, single_label

  def use_unlimit_range(self, length, label):
    # 随机给一个位置以及一个 query 向量；如果超出原本的长度，会给出 x
    # size: [74]
    pos = random.randrange(0, 9)
    pos_tensor = F.one_hot(torch.tensor(pos), num_classes=10).float()
    # pos_tensor = use_embed(pos)

    # -1 caused by ctc preprocess, for instance, digit 9 label is 10
    if pos >= length:
      # 10 means empty, works for real dataset.
      single_label = F.one_hot(torch.tensor(10), num_classes=11).float()
    else:
      # for some dataset, the label is 1-10, not 0-9. not support verify-dataset.
      # single_label = F.one_hot(label[pos] - 1, num_classes=11).float()
      # 0-9 dataset
      single_label = F.one_hot(label[pos], num_classes=11).float()

    return pos, pos_tensor, single_label

  def __getitem__(self, idx):
    image = self.imgs[idx].reshape((1, 32, 300))
    label = self.labels[idx]
    length = len(label)
    label = torch.LongTensor(label)

    # pos, pos_tensor, single_label = self.use_unlimit_range(length, label)
    if self.limit:
      pos, pos_tensor, single_label = self.use_limit_range(length, label)
    else:
      pos, pos_tensor, single_label = self.use_unlimit_range(length, label)

    # pos is query vector
    return image, pos, pos_tensor, single_label, label, length
