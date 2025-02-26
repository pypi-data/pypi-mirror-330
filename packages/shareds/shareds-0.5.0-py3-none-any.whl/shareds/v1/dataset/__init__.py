"""Move pointcnn dataset here. Avoid depends of pointcnn."""

# from collections import namedtuple
import pathlib
import random
import typing as t

import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset

from shareds.v1 import transforms

from .funcs import use_onehot
from .lmdb import LMDBLabelDataset as LD


def gen4l_collate_fn(batch):
  # image, pos, pos_tensor, label[pos], length
  images, pos, pos_tensors, labels, full_labels, lengths = zip(*batch)

  images = torch.stack(images, 0)  # images: tuple[tensor]
  labels = torch.stack(labels, 0)
  pos_tensors = torch.stack(pos_tensors, 0)
  # [batch_size, width, height, channel]
  # [batch_size, 74]
  # [batch_size, 1]

  batch_data = (images, pos_tensors, labels, full_labels, lengths)
  return batch_data[:3]


class Gen4L9MeterDataset(Dataset):
  """4w dataset, 9 digits label. This dataset is construct to img, query, label. To get more details, read the __get_item__ source code."""

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
    pos = random.randrange(0, length)
    pos_tensor = use_onehot(pos, 10)
    # pos_tensor = use_embed(pos)

    # -1 caused by ctc preprocess, for instance, digit 9 label is 10
    single_label = F.one_hot(label[pos] - 1, num_classes=10).float()

    # pos is query vector
    return image, pos, pos_tensor, single_label, label, length
