"""
PolarsDataFrameReader module.
"""
import polars as pl

from datajudge.data_reader.base_native_reader import NativeReader
from datajudge.utils.exceptions import StoreError


class PolarsDataFrameSQLReader(NativeReader):
    """
    PolarsDataFrameSQLReader class.

    It allows to read a resource as polars DataFrame.
    """

    def fetch_data(self, src: str, query: str) -> pl.DataFrame:
        """
        Fetch resource from backend.
        """
        conn_string = super().fetch_data(src)
        return self._read_df_from_db(conn_string, query)

    @staticmethod
    def _read_df_from_db(conn_str: str, query: str) -> pl.DataFrame:
        """
        Use polars to read data from db.
        """
        try:
            return pl.read_database(query, conn_str)
        except Exception as ex:
            raise StoreError(
                f"Unable to read data from query: {query}. Arguments: {str(ex.args)}"
            )
