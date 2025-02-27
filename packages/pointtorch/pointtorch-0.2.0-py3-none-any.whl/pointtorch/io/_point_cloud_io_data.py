"""Point cloud data structure used for I/O."""

__all__ = ["PointCloudIoData"]

from dataclasses import dataclass
from typing import Optional

import pandas as pd


@dataclass
class PointCloudIoData:
    """Point cloud data structure used for I/O."""

    data: pd.DataFrame
    crs: Optional[str] = None
    identifier: Optional[str] = None
    x_max_resolution: Optional[float] = None
    y_max_resolution: Optional[float] = None
    z_max_resolution: Optional[float] = None
