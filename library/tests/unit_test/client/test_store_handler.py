from pathlib import Path

import pytest

from datajudge.client.store_handler import (
    DEFAULT_STORE,
    STORE_TYPE_ARTIFACT,
    STORE_TYPE_METADATA,
    StoreHandler,
    StoreRegistry,
)
from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.store_artifact.dummy_artifact_store import DummyArtifactStore
from datajudge.store_metadata.dummy_metadata_store import DummyMetadataStore
from datajudge.store_metadata.metadata_store import MetadataStore
from datajudge.utils.commons import GENERIC_DUMMY
from datajudge.utils.exceptions import StoreError


class TestStoreRegistry:
    def test_setup(self, registry):
        dict_ = {
            STORE_TYPE_ARTIFACT: [],
            DEFAULT_STORE: None,
            STORE_TYPE_METADATA: None,
        }
        assert registry.registry == dict_

    def test_register(self, md_st, st_1, st_2, registry):
        registry.register(st_1, STORE_TYPE_ARTIFACT)
        assert registry.registry[STORE_TYPE_ARTIFACT] == [st_1]

        with pytest.raises(StoreError):
            registry.register(st_1, STORE_TYPE_ARTIFACT)

        registry.register(st_2, STORE_TYPE_ARTIFACT)
        assert registry.registry[STORE_TYPE_ARTIFACT] == [st_1, st_2]

        registry.register(md_st, STORE_TYPE_METADATA)
        assert registry.registry[STORE_TYPE_METADATA] == md_st

        registry.register(st_1, DEFAULT_STORE)
        assert registry.registry[DEFAULT_STORE] == st_1

    def test_get_store(self, md_st, st_1, registry):
        registry.register(md_st, STORE_TYPE_METADATA)
        registry.register(st_1, STORE_TYPE_ARTIFACT)
        registry.register(st_1, DEFAULT_STORE)

        store = registry.get_store(STORE_TYPE_METADATA)
        assert store == md_st
        store = registry.get_store(DEFAULT_STORE)
        assert store == st_1
        store = registry.get_store(STORE_TYPE_ARTIFACT, st_1.name)
        assert store == st_1

        with pytest.raises(StoreError):
            store = registry.get_store(STORE_TYPE_ARTIFACT, "error")
        with pytest.raises(StoreError):
            store = registry.get_store("error")

    def test_get_all_store(self, st_1, st_2, registry):
        registry.register(st_1, STORE_TYPE_ARTIFACT)
        registry.register(st_2, STORE_TYPE_ARTIFACT)
        stores = registry.get_all_stores(STORE_TYPE_ARTIFACT)
        assert len(stores) == 2


class TestStoreHandler:
    def test_setup(self, temp_data):
        handler = StoreHandler(tmp_dir=temp_data)
        assert isinstance(handler.get_md_store(), MetadataStore)
        assert isinstance(handler.get_art_store(GENERIC_DUMMY), ArtifactStore)
        assert isinstance(handler.get_def_store(), ArtifactStore)

    def test_add_metadata_store(self, temp_data, mds_cfg):
        handler = StoreHandler(tmp_dir=temp_data)
        handler._add_metadata_store(mds_cfg)
        assert isinstance(handler.get_md_store(), MetadataStore)

    def test_add_artifact_store(self, temp_data, st_loc1_cfg):
        handler = StoreHandler(tmp_dir=temp_data)
        handler.add_artifact_store(st_loc1_cfg)
        assert isinstance(handler.get_art_store(st_loc1_cfg.name), ArtifactStore)
        with pytest.raises(StoreError):
            handler.add_artifact_store(st_loc1_cfg)

    def test_update_default_store(self, temp_data, st_loc1_cfg, st_loc2_cfg):
        handler = StoreHandler(store=st_loc1_cfg, tmp_dir=temp_data)
        assert handler._update_default_store() is None

        with pytest.raises(StoreError):
            handler = StoreHandler(store=st_loc1_cfg, tmp_dir=temp_data)
            st_loc2_cfg.isDefault = True
            handler.add_artifact_store(st_loc2_cfg)
            handler._update_default_store()

        with pytest.raises(StoreError):
            st_loc1_cfg.isDefault = False
            st_loc2_cfg.isDefault = False
            handler = StoreHandler(store=[st_loc1_cfg, st_loc2_cfg], tmp_dir=temp_data)
            handler._update_default_store()

    def test_get_md_store(self, temp_data):
        assert isinstance(
            StoreHandler(tmp_dir=temp_data).get_md_store(), DummyMetadataStore
        )

    def test_get_art_store(self, temp_data):
        assert isinstance(
            StoreHandler(tmp_dir=temp_data).get_art_store(GENERIC_DUMMY),
            DummyArtifactStore,
        )

    def test_get_def_store(self, temp_data):
        assert isinstance(
            StoreHandler(tmp_dir=temp_data).get_def_store(), DummyArtifactStore
        )

    def test_get_all_art_stores(self, temp_data):
        assert isinstance(StoreHandler(tmp_dir=temp_data).get_all_art_stores(), list)

    def test_clean_all(self, tmp_path_factory):
        tmp = str(tmp_path_factory.mktemp("test"))
        StoreHandler(tmp_dir=tmp).clean_all()
        assert not Path(tmp).is_dir()

    def test_clean_temp_path_store_cache(self, temp_data, st_loc1_cfg):
        handler = StoreHandler(store=st_loc1_cfg, tmp_dir=temp_data)
        store = handler.get_art_store(st_loc1_cfg.name)
        store.resource_paths.registry = "test"
        assert store.resource_paths.registry == "test"
        handler._clean_temp_path_store_cache()
        assert store.resource_paths.registry == {}


# Metadata store config
@pytest.fixture
def mds_cfg(local_md_store_cfg):
    return local_md_store_cfg


# Artifact store config 1
@pytest.fixture
def st_loc1_cfg(local_store_cfg):
    return local_store_cfg


# Artifact store config 2
@pytest.fixture
def st_loc2_cfg(local_store_cfg_2):
    return local_store_cfg_2


# Store Registry
@pytest.fixture()
def registry():
    return StoreRegistry()


# Metadata store object
@pytest.fixture()
def md_st(store_builder, mds_cfg):
    return store_builder.build(mds_cfg)


# Artifact store object 1
@pytest.fixture()
def st_1(store_builder, st_loc1_cfg):
    return store_builder.build(st_loc1_cfg)


# Artifact store object 2
@pytest.fixture()
def st_2(store_builder, st_loc2_cfg):
    return store_builder.build(st_loc2_cfg)
