import polars as pl
import pytest

from datajudge.data_reader.polars_reader.polars_dataframe_file_reader import (
    PolarsDataFrameFileReader,
)
from tests.conftest import STORE_LOCAL_01, Configurator


@pytest.fixture()
def reader():
    conf = Configurator()
    store = conf.get_store(STORE_LOCAL_01, tmp=True)
    return PolarsDataFrameFileReader(store)


def test_fetch_data(reader):
    data = reader.fetch_data("tests/synthetic_data/test_csv_file.csv")
    assert isinstance(data, pl.DataFrame)
