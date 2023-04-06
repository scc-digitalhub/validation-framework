"""
PolarsDataFrameReader module.
"""
from pathlib import Path

import polars as pl

from datajudge.data_reader.base_file_reader import FileReader
from datajudge.plugins.utils.frictionless_utils import describe_resource
from datajudge.utils.utils import listify


class PolarsDataFrameFileReader(FileReader):
    """
    PolarsDataFrameFileReader class.

    Read a DataFrame from local file.
    """

    def fetch_data(self,
                   src: str) -> pl.DataFrame:
        """
        Fetch resource from backend.
        """
        path = super().fetch_data(src)
        return self._read_df_from_path(path)

    def _read_df_from_path(self,
                           tmp_path: str) -> pl.DataFrame:
        """
        Read a file into a Polars DataFrame.
        """
        resource = describe_resource(tmp_path)

        paths = listify(resource.get("path"))
        file_format = resource.get("format")

        if file_format == "csv":
            csv_args = {
            "separator": resource.get("dialect", {}).get("delimiter", ","),
            "encoding": resource.get("encoding", "utf8")
            }
            list_df = [pl.read_csv(Path(i), **csv_args) for i in paths]
        elif file_format == "parquet":
            list_df = [pl.read_parquet(Path(i)) for i in paths]
        else:
            raise ValueError("File extension not supported!")

        return pl.concat(list_df)
