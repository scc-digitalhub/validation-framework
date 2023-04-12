import os

import pytest

from datajudge.client.store_factory import StoreBuilder
from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.store_metadata.metadata_store import MetadataStore
from datajudge.utils.config import StoreConfig
from datajudge.utils.uri_utils import get_uri_scheme
from tests.conftest import METADATA_STORE_LOCAL, STORE_LOCAL_01, Configurator

PROJ = "test"


@pytest.fixture()
def confs():
    conf = Configurator()
    md_loc_cfg_01 = conf.get_store_cfg(METADATA_STORE_LOCAL, tmp=True)
    art_loc_cfg_01 = conf.get_store_cfg(STORE_LOCAL_01, tmp=True)
    loc = conf.get_tmp()
    builder = StoreBuilder(PROJ, loc)
    return md_loc_cfg_01, art_loc_cfg_01, builder


class TestStoreBuilder:
    def test_build(self, confs):
        md_loc_cfg_01, art_loc_cfg_01, builder = confs
        store = builder.build(md_loc_cfg_01, md_store=True)
        assert isinstance(store, MetadataStore)
        store = builder.build(art_loc_cfg_01)
        assert isinstance(store, ArtifactStore)

    def test_build_metadata_store(self, confs):
        md_loc_cfg_01, _, builder = confs
        store = builder.build_metadata_store(md_loc_cfg_01)
        assert isinstance(store, MetadataStore)

    def test_resolve_uri_metadata(self, confs):
        _, _, builder = confs
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
            new_uri = builder.resolve_uri_metadata(uri, scheme, PROJ)
            resolved_uris.append(new_uri)
        assert resolved_uris[0] == f"http://localhost:5000/api/project/{PROJ}"
        assert resolved_uris[1] == f"https://test.com/api/project/{PROJ}"
        assert resolved_uris[2] == f"{os.getcwd()}/test/metadata"
        assert resolved_uris[3] == f"/test/test/metadata"
        assert resolved_uris[4] == f"/test/metadata"

        with pytest.raises(NotImplementedError):
            uri = "fail://test"
            scheme = get_uri_scheme(uri)
            new_uri = builder.resolve_uri_metadata(uri, scheme, PROJ)

    def test_build_artifact_store(self, confs):
        _, art_loc_cfg_01, builder = confs
        store = builder.build_artifact_store(art_loc_cfg_01)
        assert isinstance(store, ArtifactStore)

    def test_resolve_artifact_uri(self, confs):
        _, _, builder = confs
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
            new_uri = builder.resolve_artifact_uri(uri, scheme)
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
            new_uri = builder.resolve_artifact_uri(uri, scheme)

    def test_check_config(self, confs):
        _, art_loc_cfg_01, builder = confs
        cfg = builder._check_config(None)
        assert isinstance(cfg, StoreConfig)
        assert cfg.type == "_dummy"

        cfg = builder._check_config(art_loc_cfg_01)
        assert isinstance(cfg, StoreConfig)
        assert cfg.type == "local"

        with pytest.raises(TypeError):
            builder._check_config([])
