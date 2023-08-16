import pandas as pd
import pytest
from sqlalchemy.engine import Engine

from datajudge.utils.exceptions import StoreError
from datajudge.utils.commons import PANDAS_DATAFRAME_SQL_READER


class TestPandasDataFrameSQLReader:
    def test_fetch_data(self, reader, sqlitedb):
        df = reader.fetch_data(sqlitedb, "select * from test")
        assert isinstance(df, pd.DataFrame)
        with pytest.raises(StoreError):
            reader.fetch_data(sqlitedb, "select not_existing from test")

    def test_get_engine(self, reader, sqlitedb):
        engine = reader._get_engine(sqlitedb)
        assert isinstance(engine, Engine)


@pytest.fixture
def store_cfg(sql_store_cfg):
    return sql_store_cfg


@pytest.fixture
def data_reader():
    return PANDAS_DATAFRAME_SQL_READER
