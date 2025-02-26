import torch
import torch.nn.functional as F


def use_onehot(pos: int, num_classes=74):
  """this function is for dataset related, like __get_item__"""
  pos_tensor = F.one_hot(torch.tensor(pos), num_classes=num_classes).float()
  return pos_tensor
