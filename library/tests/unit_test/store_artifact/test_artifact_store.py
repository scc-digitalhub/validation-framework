import pytest
from datajudge.store_artifact.artifact_store import ArtifactStore, ResourceRegistry


@pytest.fixture()
def confs():
    registry = ResourceRegistry()
    res = "res"
    path = "path"
    return registry, res, path


class TestResourceRegistry:
    def test_register(self, confs):
        registry, res, path = confs
        registry.register(res, path)

        assert registry.registry[res] == path

    def test_get_resource(self, confs):
        registry, res, path = confs
        registry.register(res, path)
        key = registry.get_resource(res)
        assert key == path
        key_err = registry.get_resource("err")
        assert key_err is None

    def test_clean_all(self, confs):
        registry, res, path = confs
        registry.register(res, path)
        registry.clean_all()
        assert registry.registry == {}


class TestArtifactStore:
    ...
