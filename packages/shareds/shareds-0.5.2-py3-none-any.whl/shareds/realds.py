"""real dataset from senario."""

import pathlib
import random
import typing as t

import numpy as np
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset

# from cnn_lstm_ctc.usetorch.shared import transforms


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


class MeterRealDataset(Dataset):
  """This dataset is construct to img, query, label. To get more details, read the __get_item__ source code.
  load label data from np file, the label 1 mapping to 1.
  The data shape is [3, 32, 300], the label shape is [11], the pos shape is [10].

  x_shape = [ 18882, 32, 192, 3,]
  y_shape = [ 18882, 6,] # [[00102], [002123]]

  __get_item__ = (image, pos, pos_tensor, single_label, label, length)
  """

  def __init__(
    self,
    root_dir: t.Union[pathlib.Path, str],
    mode: t.Literal["valid", "train", "test"],
    transforms=None,
  ):
    # h, w = (37, 297)
    if mode == "train":
      x_name = "Train/x_train_resized.npy"
      y_name = "Train/y_label.npy"
    elif mode == "valid":
      x_name = "Valid/x_train_resized.npy"
      y_name = "Valid/y_label.npy"
    else:
      raise ValueError(f"Unknown mode: {mode}")

    x_path = pathlib.Path(root_dir) / x_name
    y_path = pathlib.Path(root_dir) / y_name

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

  def __getitem__(self, idx):
    image = self.imgs[idx].reshape((3, 32, 300))
    label = self.labels[idx]
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
      single_label = F.one_hot(label[pos], num_classes=11).float()

    # pos is query vector
    return image, pos, pos_tensor, single_label, label, length
