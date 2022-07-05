"""
DataFrameReader module. It allow to read a local resource as pandas DataFrame.
"""
# pylint: disable=import-error,no-name-in-module,arguments-differ,no-member,too-few-public-methods,invalid-name
import pandas as pd
from frictionless import Resource

from datajudge.utils.utils import listify


class DataFrameReader:
    
    def __init__(self,
                 data_path: str) -> None:
        self.data_path = data_path

    def _infer_resource(self) -> dict:
        """
        Infer resource with frictionless.
        """
        # Possibily, redo this part with simple custom inference
        self.resource = Resource().describe(self.data_path,
                                            expand=True)
        self.resource.to_dict()

    def read_df(self) -> pd.DataFrame:
        """
        Read a file into a pandas DataFrame.
        """
        self._infer_resource()
        
        path = self.resource.get("path")
        file_format = self.resource.get("format", "csv")
        pandas_args = {
            "sep": self.resource.get("dialect", {}).get("delimiter", ","),
            "encoding": self.resource.get("encoding", "utf-8")
        }

        # Check if path is a list of paths
        path = listify(path)

        if file_format == "csv":
            list_df = [pd.read_csv(i, **pandas_args) for i in path]
        elif file_format in ["xls", "xlsx", "ods", "odf"]:
            list_df = [pd.read_excel(i, **pandas_args) for i in path]
        elif file_format == "parquet":
            list_df = [pd.read_parquet(i) for i in path]
        else:
            raise ValueError("File extension not supported!")
        
        return pd.concat(list_df)
