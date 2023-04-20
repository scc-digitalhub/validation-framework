import polars as pl
import pytest

from datajudge.utils.commons import POLARS_DATAFRAME_FILE_READER


def test_fetch_data(reader, data_path_csv):
    data = reader.fetch_data(data_path_csv)
    assert isinstance(data, pl.DataFrame)


@pytest.fixture
def store_cfg(local_store_cfg):
    return local_store_cfg


@pytest.fixture
def data_reader():
    return POLARS_DATAFRAME_FILE_READER
