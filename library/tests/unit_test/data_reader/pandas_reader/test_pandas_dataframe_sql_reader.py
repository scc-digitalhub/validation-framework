from pathlib import Path

import pandas as pd
import pytest
from sqlalchemy.engine import Engine

from datajudge.data_reader.pandas_reader.pandas_dataframe_sql_reader import (
    PandasDataFrameSQLReader,
)
from datajudge.utils.exceptions import StoreError
from tests.conftest import STORE_LOCAL_01, Configurator, insert_in_db


class TestPandasDataFrameSQLReader:
    conf = Configurator()
    store = conf.get_store(STORE_LOCAL_01, tmp=True)
    reader = PandasDataFrameSQLReader(store)

    db_path = Path(f"{conf.get_tmp()}", "test.db").as_posix()
    conn = f"sqlite:///{db_path}"
    insert_in_db(db_path)

    def test_fetch_data(self):
        df = self.reader.fetch_data(self.conn, "select * from test")
        assert isinstance(df, pd.DataFrame)
        with pytest.raises(StoreError):
            self.reader.fetch_data(self.conn, "select not_existing from test")

    def test_get_engine(self):
        engine = self.reader._get_engine(self.conn)
        assert isinstance(engine, Engine)
