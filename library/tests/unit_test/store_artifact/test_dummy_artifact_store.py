import pytest
from datajudge.store_artifact.dummy_artifact_store import DummyArtifactStore


class TestDummyArtifactStore:

    @pytest.fixture()
    def store(self):
        return DummyArtifactStore("", "", "", "")

    def test_persist_artifact(self, store):
        assert store.persist_artifact() is None

    def test__get_and_register_artifact(self, store):
        assert store._get_and_register_artifact() is None

    def test_fetch_file(self, store):
        assert store.fetch_file() is None

    def test_fetch_native(self, store):
        assert store.fetch_native() is None

    def test_fetch_buffer(self, store):
        assert store.fetch_buffer() is None

    def test__check_access_to_storage(self, store):
        assert store._check_access_to_storage() is None

    def test_get_run_artifacts_uri(self, store):
        assert store.get_run_artifacts_uri() is None

    def test__get_data(self, store):
        assert store._get_data() is None

    def test__store_data(self, store):
        assert store._store_data() is None
