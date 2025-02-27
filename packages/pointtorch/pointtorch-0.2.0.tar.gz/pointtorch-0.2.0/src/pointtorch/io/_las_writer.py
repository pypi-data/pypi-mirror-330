"""Point cloud file writer for las and laz files."""

__all__ = ["LasWriter"]

import pathlib
from typing import List, Optional, Union

import laspy
from laspy.compression import LazrsBackend
import numpy as np
import pandas as pd
from pyproj import CRS

from ._base_point_cloud_writer import BasePointCloudWriter
from ._point_cloud_io_data import PointCloudIoData


class LasWriter(BasePointCloudWriter):
    r"""
    Point cloud file writer for las and laz files.

    Args:
        maximum_resolution: Maximum resolution of point coordinates in meter. Corresponds to the scale parameter
            used in the las/laz compression. Larger values result in a stronger compression and lower point cloud
            resolution. Defaults to :math:`10^{-6}` m.

    Attributes:
        maximum_resolution: Maximum resolution of point coordinates in meter.
    """

    _standard_field_defaults = {"return_number": 1, "number_of_returns": 1}

    _supported_las_formats = list(range(9))

    def __init__(self, maximum_resolution: float = 1e-6) -> None:
        super().__init__()
        self.maximum_resolution = maximum_resolution

    def supported_file_formats(self) -> List[str]:
        """
        Returns:
            File formats supported by the point cloud file writer.
        """

        return ["las", "laz"]

    def _select_point_format(self, point_cloud: pd.DataFrame) -> int:
        """
        Determines the las file format that covers the most columns of the given point cloud.

        Returns:
            ID of the chosen las file format.
        """
        columns = set(point_cloud.columns).difference(["x", "y", "z"])
        best_format = 0
        covered_columns = 0

        for f in LasWriter._supported_las_formats:
            current_format = laspy.point.format.PointFormat(f)
            columns_covered_by_current_format = len(set(current_format.standard_dimension_names).intersection(columns))

            # the concept of extra dimensions is introduced in LAS 1.4 but laspy also supports extra dimensions for
            # earlier LAS versions
            # with the check f == 6, it is ensured that the LAS 1.4 specification is used if there are any extra
            # dimensions that are not covered by the standard point record formats (to adhere more stricly to the LAS
            # specification than laspy does)
            if columns_covered_by_current_format > covered_columns or f == 6:
                covered_columns = columns_covered_by_current_format
                best_format = current_format
            if covered_columns == len(columns):
                break

        return best_format

    def _write_data(  # pylint: disable=too-many-locals
        self,
        point_cloud: pd.DataFrame,
        file_path: pathlib.Path,
        *,
        crs: Optional[str] = None,
        identifier: Optional[str] = None,
        x_max_resolution: Optional[float] = None,
        y_max_resolution: Optional[float] = None,
        z_max_resolution: Optional[float] = None,
    ) -> None:
        """
        Writes a point cloud to a file.

        Args:
            point_cloud: Point cloud to be written.
            file_path: Path of the output file.
            crs: EPSG code of the coordinate reference system of the point cloud. Defaults to :code:`None`.
            identifier: Identifier of the point cloud. Defaults to :code:`None`.
            x_max_resolution: Maximum resolution of the point cloud's x-coordinates in meter. Defaults to :code:`None`.
            y_max_resolution: Maximum resolution of the point cloud's y-coordinates in meter. Defaults to :code:`None`.
            z_max_resolution: Maximum resolution of the point cloud's z-coordinates in meter. Defaults to :code:`None`.
        """

        if set(["r", "g", "b"]).issubset(point_cloud.columns) and not set(["red", "green", "blue"]).issubset(
            point_cloud.columns
        ):
            point_cloud = point_cloud.rename({"r": "red", "g": "green", "b": "blue"}, axis=1)

        las_data = laspy.create(point_format=self._select_point_format(point_cloud))
        point_coords = point_cloud[["x", "y", "z"]].values
        offsets = point_coords.min(axis=0)
        scales = [self.maximum_resolution] * 3
        if x_max_resolution is not None:
            scales[0] = x_max_resolution
        if y_max_resolution is not None:
            scales[1] = y_max_resolution
        if z_max_resolution is not None:
            scales[2] = z_max_resolution

        las_data.change_scaling(scales=scales, offsets=offsets)
        las_data.xyz = point_coords

        extra_columns = list(point_cloud.columns)

        for column_name in las_data.header.point_format.standard_dimension_names:
            if column_name.lower() in ["x", "y", "z"]:
                continue

            if column_name.lower() in point_cloud.columns:
                las_data[column_name] = point_cloud[column_name.lower()]
                extra_columns.remove(column_name)
            else:
                default_value = LasWriter._standard_field_defaults.get(column_name, 0)
                las_data[column_name] = np.full_like(las_data[column_name], fill_value=default_value)

        extra_dims = []
        for column_name in extra_columns:
            if column_name.lower() in ["x", "y", "z"]:
                continue
            extra_dims.append(laspy.point.ExtraBytesParams(column_name, point_cloud[column_name].dtype))

        las_data.add_extra_dims(extra_dims)
        las_data.update_header()

        for extra_dim in extra_dims:
            las_data[extra_dim.name] = point_cloud[extra_dim.name]

        if crs is not None:
            las_data.header.add_crs(CRS.from_string(crs))

        las_data.write(file_path, laz_backend=LazrsBackend())

    def write(
        self, point_cloud: PointCloudIoData, file_path: Union[str, pathlib.Path], columns: Optional[List[str]] = None
    ) -> None:
        """
        Writes a point cloud to a file.

        Args:
            point_cloud: Point cloud to be written.
            file_path: Path of the output file.
            columns: Point cloud columns to be written. The x, y, and z columns are always written.

        Raises:
            ValueError: If the point cloud format is not supported by the writer or if `columns` contains a column name
                that is not existing in the point cloud.
        """
        # The method from the base is called explicitly so that the read method appears in the documentation of this
        # class.
        super().write(point_cloud, file_path, columns=columns)
