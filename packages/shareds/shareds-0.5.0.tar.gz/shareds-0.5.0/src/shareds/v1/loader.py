import pathlib
import typing as t

from torch.utils.data import DataLoader, Dataset

from . import valid

METER_READING_FORMAT = t.Literal["with_empty", "no_empty", "realds"]


@valid.check_params
def get_dataset(
  data_dir: pathlib.Path,
  format: METER_READING_FORMAT,
) -> t.Tuple[Dataset, Dataset, t.Callable]:
  """Get the dataset from normal format, meter-reading format."""
  if format == "no_empty":
    from shareds.v1.dataset import Gen4L9MeterDataset, gen4l_collate_fn
  elif format == "with_empty":
    from shareds.with_empty import Gen4L9MeterDataset, gen4l_collate_fn
  elif format == "realds":
    from shareds.realds import MeterRealDataset, gen4l_collate_fn

    return (
      MeterRealDataset(root_dir=data_dir, mode="train"),
      MeterRealDataset(root_dir=data_dir, mode="valid"),
      gen4l_collate_fn,
    )

  train_dataset = Gen4L9MeterDataset(root_dir=data_dir, mode="train")
  valid_dataset = Gen4L9MeterDataset(root_dir=data_dir, mode="test")
  return train_dataset, valid_dataset, gen4l_collate_fn


def get_loader(
  data_dir: pathlib.Path,
  train_batch_size: int,
  eval_batch_size: int,
  cpu_workers: int,
  format: t.Literal["no_empty", "with_empty", "realds"],
):
  train_dataset, valid_dataset, gen4l_collate_fn = get_dataset(data_dir, format)

  train_loader = DataLoader(
    dataset=train_dataset,
    batch_size=train_batch_size,
    shuffle=True,
    num_workers=cpu_workers,
    collate_fn=gen4l_collate_fn,
  )

  valid_loader = DataLoader(
    dataset=valid_dataset,
    batch_size=eval_batch_size,
    # shuffle=True,
    num_workers=cpu_workers,
    collate_fn=gen4l_collate_fn,
  )

  return train_loader, valid_loader
