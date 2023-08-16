import polars as pl
import pytest

from datajudge.utils.exceptions import StoreError
from datajudge.utils.commons import POLARS_DATAFRAME_SQL_READER


class TestPolarsDataFrameSQLReader:
    def test_fetch_data(self, reader, sqlitedb):
        df = reader.fetch_data(sqlitedb, "select * from test")
        assert isinstance(df, pl.DataFrame)
        with pytest.raises(StoreError):
            reader.fetch_data(sqlitedb, "select not_existing from test")


@pytest.fixture
def store_cfg(sql_store_cfg):
    return sql_store_cfg


@pytest.fixture
def data_reader():
    return POLARS_DATAFRAME_SQL_READER
