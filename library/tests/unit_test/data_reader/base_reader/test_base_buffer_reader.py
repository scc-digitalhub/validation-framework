import pytest

from datajudge.utils.commons import BASE_BUFFER_READER


def test_fetch_data(reader, data_path_csv):
    with pytest.raises(NotImplementedError):
        reader.fetch_data(data_path_csv)


@pytest.fixture
def store_cfg(local_store_cfg):
    return local_store_cfg


@pytest.fixture
def data_reader():
    return BASE_BUFFER_READER
