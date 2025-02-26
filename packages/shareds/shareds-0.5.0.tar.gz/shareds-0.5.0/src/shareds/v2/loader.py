import pathlib
import typing as t

from torch.utils.data import DataLoader

from shareds.base import BaseDataset

fn = t.Callable


def get_loader(
  data_dir: pathlib.Path,
  train_batch_size: int,
  eval_batch_size: int,
  cpu_workers: int,
  get_ds_cls_fn: fn[[], tuple[fn, t.Type[BaseDataset]]],
):
  """
  获取数据集的collate函数和Dataset类。

  这个函数调用get_ds_cls_fn()来获取特定数据集的collate函数和Dataset类。
  collate函数用于将多个样本组合成一个batch，Dataset类用于定义数据集的结构和加载方式。

  返回值:
  collate_fn: 用于批处理的函数
  Dataset: 数据集类
  """
  collate_fn, Dataset = get_ds_cls_fn()

  train_dataset = Dataset(root_dir=data_dir, mode="train")
  valid_dataset = Dataset(root_dir=data_dir, mode="test")
  train_loader = DataLoader(
    dataset=train_dataset,
    batch_size=train_batch_size,
    shuffle=True,
    num_workers=cpu_workers,
    collate_fn=collate_fn,
  )

  valid_loader = DataLoader(
    dataset=valid_dataset,
    batch_size=eval_batch_size,
    # shuffle=True,
    num_workers=cpu_workers,
    collate_fn=collate_fn,
  )

  return train_loader, valid_loader
