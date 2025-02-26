# sharing dataset.

# from collections import namedtuple
import pathlib
import random
import typing as t

import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset

from .v1 import transforms
from .v1.dataset.lmdb import LMDBLabelDataset as LD


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
  load label from lmdb file, the label `1` mapping to `2`.
  The data shape is [1, 32, 300], the label shape is [11], the pos shape is [10].
  """

  def __init__(
    self,
    root_dir: t.Union[pathlib.Path, str],
    mode: t.Literal["test", "train"],
  ):
    # h, w = (37, 297)
    if mode == "train":
      x_name = "x_train.npy"
      y_name = "y_train.lmdb"
    elif mode == "test":
      x_name = "x_test.npy"
      y_name = "y_test.lmdb"

    x_path = pathlib.Path(root_dir) / x_name
    y_path = pathlib.Path(root_dir) / y_name

    self.imgs = np.load(x_path)
    self.trans_f = transforms.get_meter_transforms()
    self.imgs = self.trans_f(self.imgs)
    self.imgs = torch.FloatTensor(self.imgs)
    self.imgs = self.imgs / 255.0

    self.ldb = LD(y_path)

  def load_from_np(self, y_path):
    self.labels = np.load(y_path)
    self.labels = torch.LongTensor(self.labels)

  def __len__(self):
    return self.imgs.shape[0]

  def __getitem__(self, idx):
    image = self.imgs[idx].reshape((1, 32, 300))
    label = self.ldb[idx]
    length = len(label)
    label = torch.LongTensor(label)

    # 随机给一个位置以及一个 query 向量
    # size: [74]
    pos = random.randrange(0, 9)
    pos_tensor = F.one_hot(torch.tensor(pos), num_classes=10).float()
    # pos_tensor = use_embed(pos)

    # -1 caused by ctc preprocess, for instance, digit 9 label is 10
    if pos >= length:
      # 10 means empty, works for real dataset.
      single_label = F.one_hot(torch.tensor(10), num_classes=11).float()
    else:
      single_label = F.one_hot(label[pos] - 1, num_classes=11).float()

    # pos is query vector
    return image, pos, pos_tensor, single_label, label, length
