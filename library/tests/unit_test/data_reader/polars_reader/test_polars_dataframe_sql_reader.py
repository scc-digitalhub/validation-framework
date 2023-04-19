import polars as pl
import pytest

from datajudge.utils.exceptions import StoreError
from datajudge.utils.commons import POLARS_DATAFRAME_SQL_READER


class TestPolarsDataFrameSQLReader:
    @pytest.fixture
    def data_reader(self):
        return POLARS_DATAFRAME_SQL_READER

    def test_fetch_data(self, get_db_and_reader):
        reader, conn = get_db_and_reader
        df = reader.fetch_data(conn, "select * from test")
        assert isinstance(df, pl.DataFrame)
        with pytest.raises(StoreError):
            reader.fetch_data(conn, "select not_existing from test")
