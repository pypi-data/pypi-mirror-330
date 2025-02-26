"""save validate code here."""

import functools


def check_params(func):
  @functools.wraps(func)
  def wrapper(data_dir, format, *args, **kwargs):
    if format in ("respoincnn", "pointcnn"):
      raise ValueError(
        f"Unknown format: {format}. You should replace this with 'no_empty' or 'with_empty'"
      )
    if format not in ("no_empty", "with_empty", "realds"):
      raise ValueError(f"Unknown format: {format}")

    return func(data_dir, format, *args, **kwargs)

  return wrapper
