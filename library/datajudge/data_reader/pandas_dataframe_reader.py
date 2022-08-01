"""
PandasDataFrameReader module.
"""
from typing import IO, Optional

import pandas as pd
from frictionless import Resource
from sqlalchemy import create_engine

from datajudge.data_reader.base_reader import DataReader
from datajudge.utils.commons import SCHEME_LOCAL, SCHEME_SQL
from datajudge.utils.exceptions import StoreError
from datajudge.utils.uri_utils import get_uri_netloc, get_uri_scheme
from datajudge.utils.utils import listify


class PandasDataFrameReader(DataReader):
    """
    PandasDataFrameReader class.

    It allows to read a resource as pandas DataFrame.
    """

    def fetch_resource(self,
                       src: str,
                       query: Optional[str] = None
                       ) -> pd.DataFrame:
        """
        Fetch resource from backend.
        """
        if self.fetch_mode == self.FILE:
            path = self.store.fetch_file(src)
            return self._read_df_from_path(path)

        if self.fetch_mode == self.NATIVE:
            native_format = self.store.fetch_native(src)
            return self._read_df_from_native(native_format,
                                             src=src,
                                             query=query)
        if self.fetch_mode == self.BUFFER:
            buffer = self.store.fetch_buffer(src)
            return self._read_df_from_buffer(buffer)

        raise StoreError(
            "Please select a valid format to read file from backend.")

    @staticmethod
    def _infer_resource(path: str) -> dict:
        """
        Infer resource with frictionless.
        """
        resource = Resource().describe(path, expand=True)
        return resource.to_dict()

    def _read_df_from_path(self, tmp_path: str) -> pd.DataFrame:
        """
        Read a file into a pandas DataFrame.
        """
        resource = self._infer_resource(tmp_path)

        paths = listify(resource.get("path"))
        file_format = resource.get("format")

        if file_format == "csv":
            list_df = [pd.read_csv(i) for i in paths]
        elif file_format in ["xls", "xlsx", "ods", "odf"]:
            list_df = [pd.read_excel(i) for i in paths]
        elif file_format == "parquet":
            list_df = [pd.read_parquet(i) for i in paths]
        else:
            raise ValueError("File extension not supported!")

        return pd.concat(list_df)

    def _read_df_from_native(self,
                             native_format: str,
                             src: Optional[str] = None,
                             query: Optional[str] = None
                             ) -> pd.DataFrame:

        scheme = get_uri_scheme(native_format)

        if scheme in SCHEME_SQL:

            engine = create_engine(native_format)
            try:
                if query is not None:
                    return pd.read_sql(query, engine)
                # Get table name from path
                table = self._get_table_name(src)
                return pd.read_sql(f"SELECT * FROM {table}", engine)
            except:
                raise StoreError(f"Unable to read data from query: {query}")
            finally:
                engine.dispose()

        if scheme in SCHEME_LOCAL:
            # In local store, the native format is the path of the resource
            return self._read_df_from_path(native_format)

        raise NotImplementedError

    @staticmethod
    def _get_table_name(uri: str) -> str:
        """
        Return table name from path.
        """
        name = get_uri_netloc(uri)
        return name.split(".")[-1]

    def _read_df_from_buffer(self, path: IO) -> pd.DataFrame:
        raise NotImplementedError
