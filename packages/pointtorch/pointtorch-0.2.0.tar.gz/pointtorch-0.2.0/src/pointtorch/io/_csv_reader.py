"""Point cloud file reader for csv and txt files."""

__all__ = ["CsvReader"]

import pathlib
from typing import List, Optional, Tuple, Union

import pandas as pd

from ._base_point_cloud_reader import BasePointCloudReader
from ._point_cloud_io_data import PointCloudIoData


class CsvReader(BasePointCloudReader):
    """Point cloud file reader for csv and txt files."""

    def supported_file_formats(self) -> List[str]:
        """
        Returns:
            File formats supported by the point cloud file reader.
        """

        return ["csv", "txt"]

    def read(
        self, file_path: Union[str, pathlib.Path], columns: Optional[List[str]] = None, num_rows: Optional[int] = None
    ) -> PointCloudIoData:
        """
        Reads a point cloud file.

        Args:
            file_path: Path of the point cloud file to be read.
            columns: Name of the point cloud columns to be read. The x, y, and z columns are always read.
            num_rows: Number of rows to read. If set to :code:`None`, all rows are read. Defaults to :code:`None`.

        Returns:
            Point cloud object.

        Raises:
            ValueError: If the point cloud format is not supported by the reader.
        """
        # The method from the base is called explicitly so that the read method appears in the documentation of this
        # class.
        return super().read(file_path, columns=columns, num_rows=num_rows)

    def _read_points(
        self, file_path: pathlib.Path, columns: Optional[List[str]] = None, num_rows: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Reads point data from a point cloud file in csv or txt format.

        Args:
            file_path: Path of the point cloud file to be read.
            columns: Name of the point cloud columns to be read. The x, y, and z columns are always read.
            num_rows: Number of rows to read. If set to :code:`None`, all rows are read. Defaults to :code:`None`.

        Returns:
            Point cloud data.
        """

        file_format = file_path.suffix.lstrip(".")
        return pd.read_csv(file_path, usecols=columns, sep="," if file_format == "csv" else " ", nrows=num_rows)

    @staticmethod
    def _read_max_resolutions(file_path: pathlib.Path) -> Tuple[float, float, float]:
        """
        Reads the maximum resolution for each coordinate dimension from the point cloud file.

        Args:
            file_path: Path of the point cloud file to be read.

        Returns:
            Maximum resolution of the x-, y-, and z-coordinates of the point cloud.
        """

        file_format = file_path.suffix.lstrip(".")
        df = pd.read_csv(file_path, usecols=["x", "y", "z"], sep="," if file_format == "csv" else " ", dtype=str)

        # The precision of each coordinate is calculated by counting the digits after the decimal.
        x_max_resolution = (
            df["x"].str.split(".").apply(lambda x: round(0.1 ** len(x[1]), len(x)) if len(x) > 1 else 1).min()
        )
        y_max_resolution = (
            df["y"].str.split(".").apply(lambda x: round(0.1 ** len(x[1]), len(x)) if len(x) > 1 else 1).min()
        )
        z_max_resolution = (
            df["z"].str.split(".").apply(lambda x: round(0.1 ** len(x[1]), len(x)) if len(x) > 1 else 1).min()
        )

        return x_max_resolution, y_max_resolution, z_max_resolution
