"""This file is used to apply the model to the data."""

import abc
import pathlib

import torch

from . import loader


class MyModel(abc.ABC):
  """The model interface."""

  @abc.abstractmethod
  def predict(self, data: torch.Tensor) -> str:
    pass


def use_validate_one(
  model: MyModel,
  data_dir: pathlib.Path,
  format: loader.METER_READING_FORMAT,
):
  """Validate the model.
  model: the model to be validated.
  data_dir: the directory of the data.
  format: the format of the data.
  """
  _, valid_dataset, _ = loader.get_dataset(
    data_dir=data_dir,
    format=format,
  )

  def validate_model(index):
    import torch

    image, pos, pos_tensor, single_label, label, length = valid_dataset[index]
    # image shape: [1, 32, 128]
    image = image * 255
    image = image.to(torch.uint8)
    img = torch.cat((image, image, image), dim=0)
    return model.predict(img), img, label

  return validate_model
