import pytest

from datajudge.store_metadata.dummy_metadata_store import DummyMetadataStore


class TestDummyMetadataStore:
    def test_init_run(self, store):
        assert store.init_run("exp1", "run1", True) is None

    def test_log_metadata(self, store):
        assert store.log_metadata() is None

    def test_build_source_destination(self, store):
        assert store._build_source_destination("dst", "src_type") is None

    def test_get_run_metadata_uri(self, store):
        assert store.get_run_metadata_uri("exp1", "run1") is None


@pytest.fixture
def store():
    return DummyMetadataStore("", "", "")
