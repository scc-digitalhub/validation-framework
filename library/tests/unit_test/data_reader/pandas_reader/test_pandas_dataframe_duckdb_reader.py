import pandas as pd
import pytest

from datajudge.utils.commons import PANDAS_DATAFRAME_DUCKDB_READER
from datajudge.utils.exceptions import StoreError


def test_fetch_data(reader, tmpduckdb):
    df = reader.fetch_data(tmpduckdb, "select * from test")
    assert isinstance(df, pd.DataFrame)
    with pytest.raises(StoreError):
        reader._read_df_from_db(tmpduckdb, "select not_existing from test")


@pytest.fixture
def store_cfg(local_store_cfg):
    return local_store_cfg


@pytest.fixture(scope="module")
def data_reader():
    return PANDAS_DATAFRAME_DUCKDB_READER
