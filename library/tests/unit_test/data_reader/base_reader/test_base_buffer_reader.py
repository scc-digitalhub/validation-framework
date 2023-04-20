import pytest

from datajudge.utils.commons import BASE_BUFFER_READER


def test_fetch_data(reader, data_path):
    with pytest.raises(NotImplementedError):
        reader.fetch_data(data_path)


@pytest.fixture
def store_cfg(local_store_cfg):
    return local_store_cfg


@pytest.fixture(scope="module")
def data_reader():
    return BASE_BUFFER_READER
