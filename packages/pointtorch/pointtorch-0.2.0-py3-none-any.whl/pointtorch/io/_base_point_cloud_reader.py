"""Abstract base class for implementing point cloud file readers."""

__all__ = ["BasePointCloudReader"]

import abc
import pathlib
from typing import List, Optional, Tuple, Union

import pandas as pd

from ._point_cloud_io_data import PointCloudIoData


class BasePointCloudReader(abc.ABC):
    """Abstract base class for implementing point cloud file readers."""

    @abc.abstractmethod
    def supported_file_formats(self) -> List[str]:
        """
        Returns:
            File formats supported by the point cloud file reader.
        """

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

        if isinstance(file_path, str):
            file_path = pathlib.Path(file_path)

        file_format = file_path.suffix.lstrip(".")
        if file_format not in self.supported_file_formats():
            raise ValueError(f"The {file_format} format is not supported by the point cloud reader.")

        identifier = self._read_identifier(file_path)
        file_id = file_path.stem if identifier is None else identifier

        crs = self._read_crs(file_path)

        if columns is not None:
            columns = columns.copy()

            # The x, y, z coordinates are always loaded.
            for idx, coord in enumerate(["x", "y", "z"]):
                if coord not in columns:
                    columns.insert(idx, coord)

        point_cloud_df = self._read_points(file_path, columns=columns, num_rows=num_rows)
        (x_max_resolution, y_max_resolution, z_max_resolution) = self._read_max_resolutions(file_path)

        return PointCloudIoData(
            point_cloud_df,
            crs=crs,
            identifier=file_id,
            x_max_resolution=x_max_resolution,
            y_max_resolution=y_max_resolution,
            z_max_resolution=z_max_resolution,
        )

    @abc.abstractmethod
    def _read_points(
        self, file_path: pathlib.Path, columns: Optional[List[str]] = None, num_rows: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Reads point data from a point cloud file. This method has to be overriden by child classes.

        Args:
            file_path: Path of the point cloud file to be read.
            columns: Name of the point cloud columns to be read.
            num_rows: Number of rows to read. If set to :code:`None`, all rows are read. Defaults to :code:`None`.

        Returns:
            Point cloud data.
        """

    @staticmethod
    @abc.abstractmethod
    def _read_max_resolutions(file_path: pathlib.Path) -> Tuple[Optional[float], Optional[float], Optional[float]]:
        """
        Reads the maximum resolution for each coordinate dimension from the point cloud file.

        Args:
            file_path: Path of the point cloud file to be read.

        Returns:
            Maximum resolution of the x-, y-, and z-coordinates of the point cloud or :code:`None` if no information is
            about the maximum resolution is included in the file.
        """

    @staticmethod
    def _read_identifier(file_path: pathlib.Path) -> Optional[str]:  # pylint: disable=unused-argument
        """
        Reads the point cloud identifier from the point cloud file. Storing a file identifier is not supported by all
        file formats and :code:`None` may be returned when no file identifier is stored in a file.

        Returns:
            Point cloud identifier or :code:`None` if no file identifier is stored in the file.
        """

        return None

    @staticmethod
    def _read_crs(file_path: pathlib.Path) -> Optional[str]:  # pylint: disable=unused-argument
        """
        Reads the EPSG code of the coordinate reference system from the point cloud file. Information about the
        coordinate reference system is not supported by all file formats and :code:`None` may be returned when no
        coordinate reference system is stored in a file.

        Returns:
            EPSG code of the coordinate reference system or :code:`None` if no coordinate reference system is stored in
            the file.
        """

        return None
