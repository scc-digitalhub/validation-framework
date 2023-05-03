import pytest

from datajudge.utils.commons import (
    DATAREADER_BUFFER,
    DATAREADER_FILE,
    DATAREADER_NATIVE,
)


TEST = "test.txt"


@pytest.fixture
def store_cfg(local_store_cfg):
    return local_store_cfg


class TestLocalArtifactStore:
    def test_persist_artifact(
        self, store, temp_file, stringio, bytesio, dictionary, temp_folder
    ):
        src_name = "persist.txt"
        pth = temp_folder / src_name
        assert not pth.exists()

        # Local file
        assert not pth.exists()
        store.persist_artifact(temp_file, temp_folder, src_name)
        assert pth.exists()
        pth.unlink()

        # StringIO
        assert not pth.exists()
        store.persist_artifact(stringio, temp_folder, src_name)
        assert pth.exists()
        pth.unlink()

        # BytesIO
        assert not pth.exists()
        store.persist_artifact(bytesio, temp_folder, src_name)
        assert pth.exists()
        pth.unlink()

        # Dictionary
        assert not pth.exists()
        store.persist_artifact(dictionary, temp_folder, src_name)
        assert pth.exists()
        pth.unlink()

        # Other
        assert not pth.exists()
        with pytest.raises(NotImplementedError):
            store.persist_artifact(None, temp_folder, src_name)

        with pytest.raises(NotImplementedError):
            store.persist_artifact(dictionary, temp_folder, None)

    def test_fetch_file(self, store):
        assert store.fetch_file(TEST) == TEST

    def test_fetch_native(self, store):
        assert store.fetch_native(TEST) == TEST

    def test_fetch_buffer(self, store):
        with pytest.raises(NotImplementedError):
            store.fetch_buffer(TEST)

    @pytest.mark.parametrize(
        "src,fetch_mode,expected,not_implemented",
        [
            (TEST, DATAREADER_FILE, TEST, False),
            (TEST, DATAREADER_NATIVE, TEST, False),
            (TEST, DATAREADER_BUFFER, None, True),
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
        assert store._get_data(TEST) is None

    def test_store_data(self, store):
        assert store._store_data(TEST) is None

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

    def test_get_resource(self, store):
        assert not store._get_resource(TEST)
        store._register_resource(TEST, TEST)
        assert store._get_resource(TEST) == TEST

    def test_register_resource(self, store):
        store._register_resource(TEST, TEST)
        assert store._get_resource(TEST) == TEST

    def test_clean_paths(self, store):
        assert not store._get_resource(TEST)
        store._register_resource(TEST, TEST)
        assert store._get_resource(TEST) == TEST
        store.clean_paths()
        assert not store._get_resource(TEST)
