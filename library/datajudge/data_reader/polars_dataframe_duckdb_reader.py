"""
PolarsDataFrameDuckDBReader module.
"""
import duckdb
import polars as pl

from datajudge.data_reader.base_native_reader import NativeReader
from datajudge.utils.exceptions import StoreError


class PolarsDataFrameDuckDBReader(NativeReader):
    """
    PolarsDataFrameDuckDBReader class.

    It allows to read a resource as polars DataFrame.
    """

    def fetch_data(self, src: str, query: str) -> pl.DataFrame:
        """
        Fetch resource from backend.
        """
        return self._read_df_from_db(src, query)

    @staticmethod
    def _read_df_from_db(src: str, query: str) -> pl.DataFrame:
        """
        Use the pandas to read data from db.
        """
        try:
            # Not thread safe apparently
            conn = duckdb.connect(database=src, read_only=True)
            return conn.sql(query).pl()
        except Exception as ex:
            raise StoreError(
                f"Unable to read data from query: {query}. Arguments: {str(ex.args)}"
            )
