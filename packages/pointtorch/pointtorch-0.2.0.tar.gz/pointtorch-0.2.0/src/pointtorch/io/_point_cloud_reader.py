"""Point cloud file reader for csv, las, laz, and txt files."""

__all__ = ["PointCloudReader"]

import pathlib
from typing import List, Optional, Union

from ._csv_reader import CsvReader
from ._hdf_reader import HdfReader
from ._las_reader import LasReader
from ._point_cloud_io_data import PointCloudIoData


class PointCloudReader:
    """Point cloud file reader for csv, las, laz, and txt files."""

    def __init__(self):
        self._readers = {}
        for reader in [CsvReader(), LasReader(), HdfReader()]:
            for file_format in reader.supported_file_formats():
                self._readers[file_format] = reader

    def supported_file_formats(self) -> List[str]:
        """
        Returns:
            File formats supported by the point cloud file reader.
        """
        return list(self._readers.keys())

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
        return self._readers[file_format].read(file_path, columns=columns, num_rows=num_rows)
