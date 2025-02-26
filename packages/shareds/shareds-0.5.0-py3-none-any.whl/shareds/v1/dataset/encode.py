import typing as t

import numpy as np


def pad_arr(arr: np.ndarray, total_length: int, constant: int = 0):
  assert len(arr.shape) < 2
  length = total_length - len(arr)
  res = np.pad(arr, (0, length), "constant", constant_values=constant)
  return res.reshape(-1, total_length)


def to_int_with_filter(array: t.Iterable[str]):
  algos = [
    None,
    algo1,
    algo2,
    algo3,
  ]

  # TODO: use this version of encode strategy. load from config.
  # st = common_config["encode_strategy"]
  st = 2
  return algos[st](array)


def algo3(array: t.Iterable[str]):
  result = []
  item: str
  for item in array:
    if item == "x":
      result.append(11)
    else:
      result.append(int(item) + 1)
  return np.array(result)


def algo4(array: t.Iterable[str]):
  #
  result = []
  previous: str = ""
  item: str
  for item in array:
    if previous == item:
      result.append(0)
    if item == "x":
      # just append more blank 0 for blank label, add multiple blank label.
      result.append(10 + 1)
    else:
      result.append(int(item) + 1)
    previous = item
  return np.array(result)


def algo2(array: t.Iterable[str]):
  # problem: missing x, padding use blank is not good;
  # Use something to padding, but what?
  result = []
  item: str
  for item in array:
    if item == "x":
      pass
    else:
      result.append(int(item) + 1)
  return np.array(result)


def algo1(array: t.Iterable[str]):
  # problem: error settings. the x should not be treated as blank
  result = []
  previous: str = ""
  item: str
  for item in array:
    if item == "x":
      # just append more blank
      # 0 for blank label
      # add multiple blank label.
      result.append(0)
    else:
      if previous == item:
        result.append(0)
      result.append(int(item) + 1)
    previous = item
  return np.array(result)
