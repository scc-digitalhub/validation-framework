import pytest

from datajudge.store_metadata.dummy_metadata_store import DummyMetadataStore


@pytest.fixture()
def dummy():
    return DummyMetadataStore("", "", "")


def test_init_run(dummy):
    assert dummy.init_run("exp1", "run1", True) is None


def test_log_metadata(dummy):
    assert dummy.log_metadata() is None


def test_build_source_destination(dummy):
    assert dummy._build_source_destination("dst", "src_type") is None


def test_get_run_metadata_uri(dummy):
    assert dummy.get_run_metadata_uri("exp1", "run1") is None
