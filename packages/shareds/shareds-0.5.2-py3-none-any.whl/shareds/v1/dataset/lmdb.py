import pathlib
import sys

import lmdb

from . import encode


class LMDBLabelDataset:
  def __init__(self, root: pathlib.Path):
    self.env = lmdb.open(
      str(root),
      max_readers=1,
      readonly=True,
      lock=False,
      readahead=False,
      meminit=False,
    )

    if not self.env:
      print("cannot creat lmdb from %s" % (root))
      sys.exit(0)

    with self.env.begin(write=False) as txn:
      nSamples = int(txn.get("num-samples".encode()))
      self.nSamples = nSamples

  def __len__(self):
    return self.nSamples

  def label_tranform(self, label: str):
    return encode.algo2(label)

  def __getitem__(self, index):
    assert index <= len(self), "index range error"
    index += 1
    with self.env.begin(write=False) as txn:
      label_key = "label-%09d" % index
      label = txn.get(label_key.encode()).decode("ascii")

    label = self.label_tranform(label)
    return label
