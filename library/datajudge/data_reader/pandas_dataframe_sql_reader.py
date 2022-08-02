"""
PandasDataFrameReader module.
"""
from typing import Optional

import pandas as pd
from sqlalchemy import create_engine

from datajudge.data_reader.base_native_reader import NativeReader
from datajudge.utils.exceptions import StoreError


class PandasDataFrameSQLReader(NativeReader):
    """
    PandasDataFrameSQLReader class.

    It allows to read a resource as pandas DataFrame.
    """

    def fetch_data(self,
                   src: str,
                   query: str) -> pd.DataFrame:
        """
        Fetch resource from backend.
        """
        conn_string = super().fetch_data(src)
        return self._read_df_from_db(conn_string, query)

    def _read_df_from_db(self,
                         conn_str: str,
                         query: str) -> pd.DataFrame:
        """
        Use the pandas to read data from db.
        """
        engine = create_engine(conn_str)
        try:
            return pd.read_sql(query, engine)
        except:
            raise StoreError(f"Unable to read data from query: {query}")
        finally:
            engine.dispose()
