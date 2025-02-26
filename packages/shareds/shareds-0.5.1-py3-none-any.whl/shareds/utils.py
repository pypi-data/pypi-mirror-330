import random

import torch
import torch.nn.functional as F


def use_limit_range(length, label):
  # 随机给一个位置以及一个 query 向量, pos_tensor 中可以有没有用到的数据；限制最大长度为 7
  pos = random.randrange(0, 7)
  pos_tensor = F.one_hot(torch.tensor(pos), num_classes=10).float()

  # 0-9 map to 0-9, x map to 10
  single_label = F.one_hot(label[pos], num_classes=11).float()

  return pos, pos_tensor, single_label


def use_unlimit_range(length, label):
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
