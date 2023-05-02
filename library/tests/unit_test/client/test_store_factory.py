import os

import pytest

from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.store_metadata.metadata_store import MetadataStore
from datajudge.utils.config import StoreConfig
from datajudge.utils.uri_utils import get_uri_scheme


PROJ = "test"


class TestStoreBuilder:
    def test_build(self, store_builder, mds_cfg, st_loc1):
        store = store_builder.build(mds_cfg, md_store=True)
        assert isinstance(store, MetadataStore)
        store = store_builder.build(st_loc1)
        assert isinstance(store, ArtifactStore)

    def test_build_metadata_store(self, mds_cfg, store_builder):
        store = store_builder.build_metadata_store(mds_cfg)
        assert isinstance(store, MetadataStore)

    def test_resolve_uri_metadata(self, store_builder):
        uris = [
            "http://localhost:5000",
            "https://test.com",
            "./test",
            "/test/test",
            "file:///test",
        ]

        resolved_uris = []
        for uri in uris:
            scheme = get_uri_scheme(uri)
            new_uri = store_builder.resolve_uri_metadata(uri, scheme, PROJ)
            resolved_uris.append(new_uri)
        assert resolved_uris[0] == f"http://localhost:5000/api/project/{PROJ}"
        assert resolved_uris[1] == f"https://test.com/api/project/{PROJ}"
        assert resolved_uris[2] == f"{os.getcwd()}/test/metadata"
        assert resolved_uris[3] == f"/test/test/metadata"
        assert resolved_uris[4] == f"/test/metadata"

        with pytest.raises(NotImplementedError):
            uri = "fail://test"
            scheme = get_uri_scheme(uri)
            new_uri = store_builder.resolve_uri_metadata(uri, scheme, PROJ)

    def test_build_artifact_store(self, store_builder, st_loc1):
        store = store_builder.build_artifact_store(st_loc1)
        assert isinstance(store, ArtifactStore)

    def test_resolve_artifact_uri(self, store_builder):
        uris = [
            "./test",
            "/test/test",
            "file:///test",
            "wasb://test/test",
            "wasbs://test/test",
            "s3://test/test",
            "ftp://test/test",
            "http://localhost:5000",
            "https://test.com",
            "sql://test.test",
            "dremio://test.test",
            "odbc://test.test",
        ]

        resolved_uris = []
        for uri in uris:
            scheme = get_uri_scheme(uri)
            new_uri = store_builder.resolve_artifact_uri(uri, scheme)
            resolved_uris.append(new_uri)
        assert resolved_uris[0] == f"{os.getcwd()}/test/artifact"
        assert resolved_uris[1] == "/test/test/artifact"
        assert resolved_uris[2] == "/test/artifact"
        assert resolved_uris[3] == "wasb://test/test/artifact"
        assert resolved_uris[4] == "wasbs://test/test/artifact"
        assert resolved_uris[5] == "s3://test/test/artifact"
        assert resolved_uris[6] == "ftp://test/test/artifact"
        assert resolved_uris[7] == "http://localhost:5000"
        assert resolved_uris[8] == "https://test.com"
        assert resolved_uris[9] == "sql://test.test"
        assert resolved_uris[10] == "dremio://test.test"
        assert resolved_uris[11] == "odbc://test.test"

        with pytest.raises(NotImplementedError):
            uri = "fail://test"
            scheme = get_uri_scheme(uri)
            new_uri = store_builder.resolve_artifact_uri(uri, scheme)

    def test_check_config(self, store_builder, st_loc1):
        cfg = store_builder._check_config(None)
        assert isinstance(cfg, StoreConfig)
        assert cfg.type == "_dummy"

        cfg = store_builder._check_config(st_loc1)
        assert isinstance(cfg, StoreConfig)
        assert cfg.type == "local"

        with pytest.raises(TypeError):
            store_builder._check_config([])


# Metadata store config
@pytest.fixture
def mds_cfg(local_md_store_cfg):
    return local_md_store_cfg


# Artifact store config
@pytest.fixture
def st_loc1(local_store_cfg):
    return local_store_cfg
