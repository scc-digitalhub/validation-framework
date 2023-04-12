import pytest

from datajudge.data_reader.base_file_reader import FileReader
from tests.conftest import STORE_LOCAL_01, Configurator


@pytest.fixture()
def reader():
    conf = Configurator()
    store = conf.get_store(STORE_LOCAL_01, tmp=True)
    return FileReader(store)


def test_fetch_data(reader):
    data_path = "tests/synthetic_data/test_csv_file.csv"
    path = reader.fetch_data(data_path)
    assert path == data_path
