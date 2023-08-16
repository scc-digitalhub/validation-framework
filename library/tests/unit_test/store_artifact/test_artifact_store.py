import io

import pytest

from datajudge.store_artifact.artifact_store import ArtifactStore, ResourceRegistry
from tests.conftest import TEST_FILENAME


class TestResourceRegistry:
    def test_register(self, registry):
        registry.register("resource", "path")
        assert registry.registry["resource"] == "path"

    def test_get_resource(self, registry):
        registry.register("resource", "path")
        key = registry.get_resource("resource")
        assert key == "path"
        key_err = registry.get_resource("err")
        assert key_err is None

    def test_clean_all(self, registry):
        registry.register("resource", "path")
        registry.clean_all()
        assert registry.registry == {}


class TestArtifactStore:
    def test_get_run_artifacts_uri(self, store, temp_folder):
        assert store.get_run_artifacts_uri("test", "test") == "test/test"

    def test_get_resource(self, store):
        assert not store._get_resource(TEST_FILENAME)
        store._register_resource(TEST_FILENAME, TEST_FILENAME)
        assert store._get_resource(TEST_FILENAME) == TEST_FILENAME

    def test_register_resource(self, store):
        store._register_resource(TEST_FILENAME, TEST_FILENAME)
        assert store._get_resource(TEST_FILENAME) == TEST_FILENAME

    def test_clean_paths(self, store):
        assert not store._get_resource(TEST_FILENAME)
        store._register_resource(TEST_FILENAME, TEST_FILENAME)
        assert store._get_resource(TEST_FILENAME) == TEST_FILENAME
        store.clean_paths()
        assert not store._get_resource(TEST_FILENAME)


class ArtifactStoreSample(ArtifactStore):
    def persist_artifact(self, *args, **kwargs):
        ...

    def _get_and_register_artifact(self, *args, **kwargs):
        ...

    def _get_data(self, *args, **kwargs):
        ...

    def _store_data(self, *args, **kwargs):
        ...

    def _check_access_to_storage(self, *args, **kwargs):
        ...


@pytest.fixture
def registry():
    return ResourceRegistry()


@pytest.fixture
def store():
    return ArtifactStoreSample("", "", "", "")
