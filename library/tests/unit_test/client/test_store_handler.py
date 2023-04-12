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
from tests.conftest import (
    METADATA_STORE_LOCAL,
    STORE_LOCAL_01,
    STORE_LOCAL_02,
    Configurator,
)


@pytest.fixture()
def confs() -> None:
    conf = Configurator()
    loc = conf.get_tmp()
    md_loc_01 = conf.get_store(METADATA_STORE_LOCAL, tmp=True)
    st_loc_01 = conf.get_store(STORE_LOCAL_01, tmp=True)
    st_loc_02 = conf.get_store(STORE_LOCAL_02, tmp=True)
    return loc, md_loc_01, st_loc_01, st_loc_02


@pytest.fixture()
def registry():
    return StoreRegistry()


class TestStoreRegistry:
    def test_setup(self, registry):
        dict_ = {
            STORE_TYPE_ARTIFACT: [],
            DEFAULT_STORE: None,
            STORE_TYPE_METADATA: None,
        }
        assert registry.registry == dict_

    def test_register(self, confs, registry):
        _, md_loc_01, st_loc_01, st_loc_02 = confs

        registry.register(st_loc_01, STORE_TYPE_ARTIFACT)
        assert registry.registry[STORE_TYPE_ARTIFACT] == [st_loc_01]

        with pytest.raises(StoreError):
            registry.register(st_loc_01, STORE_TYPE_ARTIFACT)

        registry.register(st_loc_02, STORE_TYPE_ARTIFACT)
        assert registry.registry[STORE_TYPE_ARTIFACT] == [st_loc_01, st_loc_02]

        registry.register(md_loc_01, STORE_TYPE_METADATA)
        assert registry.registry[STORE_TYPE_METADATA] == md_loc_01

        registry.register(st_loc_01, DEFAULT_STORE)
        assert registry.registry[DEFAULT_STORE] == st_loc_01

    def test_get_store(self, confs, registry):
        _, md_loc_01, st_loc_01, _ = confs
        registry.register(md_loc_01, STORE_TYPE_METADATA)
        registry.register(st_loc_01, STORE_TYPE_ARTIFACT)
        registry.register(st_loc_01, DEFAULT_STORE)

        store = registry.get_store(STORE_TYPE_METADATA)
        assert store == md_loc_01
        store = registry.get_store(DEFAULT_STORE)
        assert store == st_loc_01
        store = registry.get_store(STORE_TYPE_ARTIFACT, st_loc_01.name)
        assert store == st_loc_01

        with pytest.raises(StoreError):
            store = registry.get_store(STORE_TYPE_ARTIFACT, "error")
        with pytest.raises(StoreError):
            store = registry.get_store("error")

    def test_get_all_store(self, confs, registry):
        _, _, st_loc_01, st_loc_02 = confs
        registry.register(st_loc_01, STORE_TYPE_ARTIFACT)
        registry.register(st_loc_02, STORE_TYPE_ARTIFACT)
        stores = registry.get_all_stores(STORE_TYPE_ARTIFACT)
        assert len(stores) == 2


@pytest.fixture()
def cfgconfs() -> None:
    conf = Configurator()
    loc = conf.get_tmp()
    md_loc_cfg_01 = conf.get_store_cfg(METADATA_STORE_LOCAL, tmp=True)
    st_loc_cfg_01 = conf.get_store_cfg(STORE_LOCAL_01, tmp=True)
    st_loc_cfg_02 = conf.get_store_cfg(STORE_LOCAL_02, tmp=True)
    return loc, md_loc_cfg_01, st_loc_cfg_01, st_loc_cfg_02


class TestStoreHandler:
    def test_setup(self, cfgconfs):
        loc, _, _, _ = cfgconfs
        handler = StoreHandler(tmp_dir=loc)
        assert isinstance(handler.get_md_store(), MetadataStore)
        assert isinstance(handler.get_art_store(GENERIC_DUMMY), ArtifactStore)
        assert isinstance(handler.get_def_store(), ArtifactStore)

    def test_add_metadata_store(self, cfgconfs):
        loc, md_loc_cfg_01, _, _ = cfgconfs
        handler = StoreHandler(tmp_dir=loc)
        handler._add_metadata_store(md_loc_cfg_01)
        assert isinstance(handler.get_md_store(), MetadataStore)

    def test_add_artifact_store(self, cfgconfs):
        loc, _, st_loc_cfg_01, _ = cfgconfs
        handler = StoreHandler(tmp_dir=loc)
        handler.add_artifact_store(st_loc_cfg_01)
        assert isinstance(handler.get_art_store(st_loc_cfg_01.name), ArtifactStore)
        with pytest.raises(StoreError):
            handler.add_artifact_store(st_loc_cfg_01)

    def test_update_default_store(self, cfgconfs):
        loc, _, st_loc_cfg_01, st_loc_cfg_02 = cfgconfs
        handler = StoreHandler(store=st_loc_cfg_01, tmp_dir=loc)
        assert handler._update_default_store() is None

        with pytest.raises(StoreError):
            handler = StoreHandler(store=st_loc_cfg_01, tmp_dir=loc)
            st_loc_cfg_02.isDefault = True
            handler.add_artifact_store(st_loc_cfg_02)
            handler._update_default_store()

        with pytest.raises(StoreError):
            st_loc_cfg_01.isDefault = False
            st_loc_cfg_02.isDefault = False
            handler = StoreHandler(store=[st_loc_cfg_01, st_loc_cfg_02], tmp_dir=loc)
            handler._update_default_store()

    def test_get_md_store(self, cfgconfs):
        loc, _, _, _ = cfgconfs
        assert isinstance(StoreHandler(tmp_dir=loc).get_md_store(), DummyMetadataStore)

    def test_get_art_store(self, cfgconfs):
        loc, _, _, _ = cfgconfs
        assert isinstance(
            StoreHandler(tmp_dir=loc).get_art_store(GENERIC_DUMMY),
            DummyArtifactStore,
        )

    def test_get_def_store(self, cfgconfs):
        loc, _, _, _ = cfgconfs
        assert isinstance(StoreHandler(tmp_dir=loc).get_def_store(), DummyArtifactStore)

    def test_get_all_art_stores(self, cfgconfs):
        loc, _, _, _ = cfgconfs
        assert isinstance(StoreHandler(tmp_dir=loc).get_all_art_stores(), list)

    def test_clean_all(self, cfgconfs):
        loc, _, _, _ = cfgconfs
        StoreHandler(tmp_dir=loc).clean_all()
        assert not Path(loc).is_dir()

    def test_clean_temp_path_store_cache(self, cfgconfs):
        loc, _, st_loc_cfg_01, _ = cfgconfs
        handler = StoreHandler(store=st_loc_cfg_01, tmp_dir=loc)
        store = handler.get_art_store(st_loc_cfg_01.name)
        store.resource_paths.registry = "test"
        assert store.resource_paths.registry == "test"
        handler._clean_temp_path_store_cache()
        assert store.resource_paths.registry == {}
