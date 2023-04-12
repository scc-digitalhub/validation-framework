import pytest

from datajudge.data_reader.base_native_reader import NativeReader
from tests.conftest import STORE_LOCAL_01, Configurator


@pytest.fixture()
def reader():
    conf = Configurator()
    store = conf.get_store(STORE_LOCAL_01, tmp=True)
    return NativeReader(store)


def test_fetch_data(reader):
    path = reader.fetch_data("../../synthetic_data/test_csv_file.csv")
    assert path == "../../synthetic_data/test_csv_file.csv"
