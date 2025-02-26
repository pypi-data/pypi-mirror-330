import torch
from torchvision.transforms import v2


# TODO: 与shareds.v1.transforms.py合并
class Transforms(object):
  def get_meter_transforms(self):
    """get meter specific transforms"""
    return v2.Compose(
      [
        v2.ToDtype(torch.float32, scale=True),
        # v2.Normalize(mean=[0, 0, 0], std=[255, 255, 255]),
        # might problem with gray image.
        # v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
      ]
    )


transforms = Transforms()
