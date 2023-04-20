import pytest

from datajudge.utils.commons import BASE_FILE_READER


def test_fetch_data(reader, data_path):
    path = reader.fetch_data(data_path)
    assert path == data_path


@pytest.fixture
def store_cfg(local_store_cfg):
    return local_store_cfg


@pytest.fixture(scope="module")
def data_reader():
    return BASE_FILE_READER
