from pathlib import Path

import duckdb
import polars as pl
import pytest

from datajudge.data_reader.polars_dataframe_duckdb_reader import (
    PolarsDataFrameDuckDBReader,
)
from datajudge.utils.exceptions import StoreError
from tests.conftest import STORE_LOCAL_01, Configurator


def test_fetch_data():
    # Get reader
    conf = Configurator()
    store = conf.get_store(STORE_LOCAL_01, tmp=True)
    reader = PolarsDataFrameDuckDBReader(store)

    # Get tmp db path
    name = conf.get_tmp()
    Path(name).touch("test.duckdb")
    db_path = Path(name, "test.duckdb").as_posix()

    # Write in db
    conn = duckdb.connect(database=db_path, read_only=False)
    data_path = "tests/synthetic_data/test_csv_file.csv"
    conn.execute(f"CREATE TABLE test AS SELECT * FROM '{data_path}';")
    conn.close()

    df = reader.fetch_data(db_path, "select * from test")
    assert isinstance(df, pl.DataFrame)
    with pytest.raises(StoreError):
        reader._read_df_from_db(db_path, "select not_existing from test")
