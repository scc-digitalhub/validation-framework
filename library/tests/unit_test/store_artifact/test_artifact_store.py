import io

import pytest
from datajudge.store_artifact.artifact_store import ArtifactStore, ResourceRegistry


@pytest.fixture
def registry():
    return ResourceRegistry()


@pytest.fixture
def res():
    return "res"


@pytest.fixture
def path():
    return "path"


class TestResourceRegistry:
    def test_register(self, registry, res, path):
        registry.register(res, path)
        assert registry.registry[res] == path

    def test_get_resource(self, registry, res, path):
        registry.register(res, path)
        key = registry.get_resource(res)
        assert key == path
        key_err = registry.get_resource("err")
        assert key_err is None

    def test_clean_all(self, registry, res, path):
        registry.register(res, path)
        registry.clean_all()
        assert registry.registry == {}


class TestArtifactStore:
    def test_persist_artifact(self):
        ...

    def test_fetch_file(self):
        ...

    def test_fetch_native(self):
        ...

    def test_fetch_buffer(self):
        ...

    def test__get_and_register_artifact(self):
        ...

    def test__get_data(self):
        ...

    def test__store_data(self):
        ...

    def test__check_access_to_storage(self):
        ...

    def test_get_run_artifacts_uri(self):
        ...

    def test__get_resource(self):
        ...

    def test__register_resource(self):
        ...

    def test_clean_paths(self):
        ...
