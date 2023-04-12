from pathlib import Path

import polars as pl
import pytest

from datajudge.data_reader.polars_dataframe_sql_reader import PolarsDataFrameSQLReader
from datajudge.utils.exceptions import StoreError
from tests.conftest import STORE_LOCAL_01, Configurator, insert_in_db


class TestPolarsDataFrameSQLReader:
    conf = Configurator()
    store = conf.get_store(STORE_LOCAL_01, tmp=True)
    reader = PolarsDataFrameSQLReader(store)

    db_path = Path(f"{conf.get_tmp()}", "test.db").as_posix()
    conn = f"sqlite:///{db_path}"
    insert_in_db(db_path)

    def test_fetch_data(self):
        df = self.reader.fetch_data(self.conn, "select * from test")
        assert isinstance(df, pl.DataFrame)
        with pytest.raises(StoreError):
            self.reader.fetch_data(self.conn, "select not_existing from test")
