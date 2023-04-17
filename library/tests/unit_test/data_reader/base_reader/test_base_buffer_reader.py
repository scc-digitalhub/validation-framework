import pytest

from datajudge.data_reader.base_reader.base_buffer_reader import BufferReader
from tests.conftest import STORE_LOCAL_01, Configurator


@pytest.fixture()
def reader():
    conf = Configurator()
    store = conf.get_store(STORE_LOCAL_01, tmp=True)
    return BufferReader(store)


def test_fetch_data(reader):
    with pytest.raises(NotImplementedError):
        reader.fetch_data("tests/synthetic_data/test_csv_file.csv")
