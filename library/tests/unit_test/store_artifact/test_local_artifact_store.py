import pytest

from datajudge.utils.commons import (
    DATAREADER_BUFFER,
    DATAREADER_FILE,
    DATAREADER_NATIVE,
)
from tests.conftest import TEST_FILENAME


class TestLocalArtifactStore:
    def test_persist_artifact(
        self, store, temp_file, stringio, bytesio, dictionary, temp_folder
    ):
        src_name = "persist.txt"
        pth = temp_folder / src_name

        # Local file
        not_exists(pth)
        store.persist_artifact(temp_file, temp_folder, src_name)
        exists(pth)

        # StringIO
        not_exists(pth)
        store.persist_artifact(stringio, temp_folder, src_name)
        exists(pth)

        # BytesIO
        not_exists(pth)
        store.persist_artifact(bytesio, temp_folder, src_name)
        exists(pth)

        # Dictionary
        not_exists(pth)
        store.persist_artifact(dictionary, temp_folder, src_name)
        exists(pth)

        # Other
        not_exists(pth)
        with pytest.raises(NotImplementedError):
            store.persist_artifact(None, temp_folder, src_name)

        with pytest.raises(NotImplementedError):
            store.persist_artifact(dictionary, temp_folder, None)

    def test_fetch_file(self, store):
        assert store.fetch_file(TEST_FILENAME) == TEST_FILENAME

    def test_fetch_native(self, store):
        assert store.fetch_native(TEST_FILENAME) == TEST_FILENAME

    def test_fetch_buffer(self, store):
        with pytest.raises(NotImplementedError):
            store.fetch_buffer(TEST_FILENAME)

    @pytest.mark.parametrize(
        "src,fetch_mode,expected,not_implemented",
        [
            (TEST_FILENAME, DATAREADER_FILE, TEST_FILENAME, False),
            (TEST_FILENAME, DATAREADER_NATIVE, TEST_FILENAME, False),
            (TEST_FILENAME, DATAREADER_BUFFER, None, True),
        ],
    )
    def test_get_and_register_artifact(
        self, store, src, fetch_mode, expected, not_implemented
    ):
        if not_implemented:
            with pytest.raises(NotImplementedError):
                store._get_and_register_artifact(src, fetch_mode)
        else:
            res = store._get_and_register_artifact(src, fetch_mode)
            assert res == expected
            assert res == store._get_resource(f"{src}_{fetch_mode}")

    def test_get_data(self, store):
        assert store._get_data(TEST_FILENAME) is None

    def test_store_data(self, store):
        assert store._store_data(TEST_FILENAME) is None

    def test_check_access_to_storage(self, store, temp_folder):
        fld = temp_folder / "fld"
        store._check_access_to_storage(fld)
        assert not fld.exists()
        store._check_access_to_storage(fld, write=True)
        assert fld.exists()

    def test_get_run_artifacts_uri(self, store, temp_folder):
        pth = str(temp_folder / "artifact" / "test" / "test")
        assert store.get_run_artifacts_uri("test", "test") == pth
        pth = str(temp_folder / "artifact" / "test1" / "test2")
        assert store.get_run_artifacts_uri("test1", "test2") == pth


@pytest.fixture
def store_cfg(local_store_cfg):
    return local_store_cfg


def exists(pth):
    assert pth.exists()
    pth.unlink()


def not_exists(pth):
    assert not pth.exists()
