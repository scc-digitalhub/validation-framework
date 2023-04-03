"""
PandasDataFrameReader module.
"""
import pandas as pd

from datajudge.data_reader.base_file_reader import FileReader
from datajudge.plugins.utils.frictionless_utils import describe_resource
from datajudge.utils.utils import listify


class PandasDataFrameFileReader(FileReader):
    """
    PandasDataFrameFileReader class.

    Read a DataFrame from local file.
    """

    def fetch_data(self,
                   src: str) -> pd.DataFrame:
        """
        Fetch resource from backend.
        """
        path = super().fetch_data(src)
        return self._read_df_from_path(path)

    def _read_df_from_path(self, tmp_path: str) -> pd.DataFrame:
        """
        Read a file into a pandas DataFrame.
        """
        resource = describe_resource(tmp_path)

        paths = listify(resource.get("path"))
        file_format = resource.get("format")

        if file_format == "csv":
            csv_args = {
            "sep": resource.get("dialect", {}).get("delimiter", ","),
            "encoding": resource.get("encoding")
            }
            list_df = [pd.read_csv(i, **csv_args) for i in paths]
        elif file_format in ["xls", "xlsx", "ods", "odf"]:
            list_df = [pd.read_excel(i) for i in paths]
        elif file_format == "parquet":
            list_df = [pd.read_parquet(i) for i in paths]
        else:
            raise ValueError("File extension not supported!")

        return pd.concat(list_df)
