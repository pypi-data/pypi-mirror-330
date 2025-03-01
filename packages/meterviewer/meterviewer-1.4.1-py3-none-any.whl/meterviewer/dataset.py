"""
Using MeterSet to construct torch dataset

Args:
  root_dir: root directory of the dataset
  stage: train or test
  train_folder: train folder name
  train_list: train list
"""

import pathlib
import warnings

try:
  from torch.utils.data import Dataset
except ImportError:
  warnings.warn(
    "torch is not installed. Please install it with `pip install torch`.", stacklevel=2
  )

  class Dataset:
    pass


from meterviewer.meterset import MeterSet


class MyMeterSet(MeterSet):
  def __str__(self):
    return f"MeterSet(name={self.name}, root_path={self.root_path})"

  def __len__(self):
    return len(self.image_list)


class MeterDataset(Dataset):
  def __init__(
    self,
    root_dir,
    stage: str,
    transform=None,
  ):
    self.root_dir = root_dir
    self.stage = stage
    self.transform = transform
    self.load_metersets()
    self.length = sum([self.get_len(meterset) for meterset in self.metersets])
    self.start_end_list = self.scan()

  def load_metersets(self):
    raise NotImplementedError("Please implement this method")

  def build_metersets(
    self,
    train_list: list[str],
    train_folder: str,
    test_list: list[str],
    test_folder: str,
  ):
    if self.stage == "train":
      self.metersets = [
        MyMeterSet(name=name, root_path=pathlib.Path(self.root_dir) / train_folder)
        for name in train_list
      ]
    elif self.stage == "test":
      self.metersets = [
        MyMeterSet(name=name, root_path=pathlib.Path(self.root_dir) / test_folder)
        for name in test_list
      ]

  def get_len(self, meterset: MeterSet):
    return len(meterset)

  def __len__(self):
    return self.length

  def check(self):
    for meterset in self.metersets:
      assert len(meterset.image_list) > 0, meterset

  def get_item(self, meterset, index):
    """get item from one metersets"""
    sample = {
      "image": meterset.images(index),
      "values": meterset.values(index),
      "pos": meterset.pos(index),
    }
    if self.transform is not None:
      sample = self.transform(sample)
    return sample

  def scan(self):
    """扫描 metersets，返回一个开始结束索引的列表，__getitem__ 可以借助这个列表来快速定位"""
    start_end_list = []
    for i, meterset in enumerate(self.metersets):
      start_end_list.append(
        (
          sum(self.get_len(meterset) for meterset in self.metersets[:i]),
          sum(self.get_len(meterset) for meterset in self.metersets[: i + 1]),
        )
      )
    return start_end_list

  def __getitem__(self, index):
    """get item from all over the metersets"""
    for i, (start, end) in enumerate(self.start_end_list):
      if start <= index < end:
        return self.get_item(self.metersets[i], index - start)
    raise IndexError(f"index {index} out of range")
