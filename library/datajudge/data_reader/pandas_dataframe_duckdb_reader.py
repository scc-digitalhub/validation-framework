"""
PandasDataFrameDuckDBReader module.
"""
import duckdb
import pandas as pd

from datajudge.data_reader.base_native_reader import NativeReader
from datajudge.utils.exceptions import StoreError


class PandasDataFrameDuckDBReader(NativeReader):
    """
    PandasDataFrameDuckDBReader class.

    It allows to read a resource as pandas DataFrame.
    """

    def fetch_data(self,
                   src: str,
                   query: str) -> pd.DataFrame:
        """
        Fetch resource from backend.
        """
        return self._read_df_from_db(src, query)

    @staticmethod
    def _read_df_from_db(src: str,
                         query: str) -> pd.DataFrame:
        """
        Use the pandas to read data from db.
        """
        try:
            conn = duckdb.connect(database=src, read_only=True)
            conn.execute(query)
            return conn.fetchdf()
        except Exception as ex:
            raise StoreError(
                f"Unable to read data from query: {query}. Arguments: {str(ex.args)}")
