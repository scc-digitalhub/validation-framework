import pandas as pd
import pytest

from datajudge.data_reader.pandas_reader.pandas_dataframe_file_reader import (
    PandasDataFrameFileReader,
)
from tests.conftest import STORE_LOCAL_01, Configurator


@pytest.fixture()
def reader():
    conf = Configurator()
    store = conf.get_store(STORE_LOCAL_01, tmp=True)
    return PandasDataFrameFileReader(store)


def test_fetch_data(reader):
    data = reader.fetch_data("tests/synthetic_data/test_csv_file.csv")
    assert isinstance(data, pd.DataFrame)
