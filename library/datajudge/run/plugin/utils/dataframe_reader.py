"""
DataFrameReader module.
"""

import pandas as pd
from frictionless import Resource

from datajudge.utils.utils import listify


class DataFrameReader:
    """
    DataFrameReader class.

    It allows to read a local resource as pandas DataFrame.
    """

    def __init__(self,
                 data_path: str) -> None:
        self.data_path = data_path

    def _infer_resource(self) -> dict:
        """
        Infer resource with frictionless.
        """
        # Possibily, redo this part with simple custom inference
        resource = Resource().describe(self.data_path,
                                       expand=True)
        return resource.to_dict()

    def read_df(self) -> pd.DataFrame:
        """
        Read a file into a pandas DataFrame.
        """
        resource = self._infer_resource()

        path = resource.get("path")
        file_format = resource.get("format", "csv")

        # Check if path is a list of paths
        path = listify(path)

        if file_format == "csv":
            csv_args = {
            "sep": resource.get("dialect", {}).get("delimiter", ","),
            "encoding": resource.get("encoding", "utf-8")
            }
            list_df = [pd.read_csv(i, **csv_args) for i in path]
        elif file_format in ["xls", "xlsx", "ods", "odf"]:
            list_df = [pd.read_excel(i) for i in path]
        elif file_format == "parquet":
            list_df = [pd.read_parquet(i) for i in path]
        else:
            raise ValueError("File extension not supported!")

        return pd.concat(list_df)
