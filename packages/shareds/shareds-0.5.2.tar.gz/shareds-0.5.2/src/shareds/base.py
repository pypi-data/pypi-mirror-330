import pathlib
import typing as t

import numpy as np
import torch
from torch.utils.data import Dataset


class ImageShaper(object):
  """This class is used to shape the image to the desired shape."""

  @property
  def img_shape(self) -> tuple[int, int, int]:
    if not hasattr(self, "_img_shape"):
      raise AttributeError("You must set img_shape first")
    return self._img_shape

  def set_img_shape(self, img_shape: tuple[int, int, int]):
    self._img_shape = img_shape


class BaseDataset(Dataset, ImageShaper):
  def __init__(
    self,
    root_dir: t.Union[pathlib.Path, str],
    mode: t.Literal["test", "train"],
    transforms: t.Callable,
  ) -> None:
    if mode == "train":
      x_name = "x_train.npy"
      y_name = "y_train.npy"
    elif mode == "test":
      x_name = "x_test.npy"
      y_name = "y_test.npy"

    x_path = pathlib.Path(root_dir) / x_name
    y_path = pathlib.Path(root_dir) / y_name
    self.imgs = np.load(x_path)
    self.trans_f = transforms

    self.imgs = self.trans_f(self.imgs)
    self.imgs = torch.FloatTensor(self.imgs)
    self.imgs = self.imgs / 255.0

    self.labels = np.load(y_path)

  def generate_label(self, length, label) -> tuple[int, torch.Tensor, torch.Tensor]:
    raise NotImplementedError("You must implement this method")

  def __getitem__(self, idx):
    image = self.imgs[idx].reshape(self.img_shape)
    label = self.labels[idx]
    length = len(label)
    label = torch.LongTensor(label)

    pos, pos_tensor, single_label = self.generate_label(length, label)

    # pos is query vector
    return image, pos, pos_tensor, single_label, label, length

  def __len__(self):
    return len(self.imgs)
