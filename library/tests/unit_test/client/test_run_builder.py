from pathlib import Path

import pytest

from datajudge.client.run_builder import RunBuilder
from datajudge.client.store_handler import StoreHandler
from datajudge.run.run import Run
from datajudge.utils.exceptions import RunError
from tests.conftest import (
    METADATA_STORE_LOCAL,
    RES_LOCAL_01,
    RUN_CFG_EMPTY,
    STORE_LOCAL_01,
    Configurator,
)


@pytest.fixture()
def st_confs():
    conf = Configurator()
    loc = conf.get_tmp()
    md_loc_cfg_01 = conf.get_store_cfg(METADATA_STORE_LOCAL, tmp=True)
    art_loc_cfg_01 = conf.get_store_cfg(STORE_LOCAL_01, tmp=True)
    return md_loc_cfg_01, art_loc_cfg_01, loc


@pytest.fixture()
def build_builder_local(st_confs):
    md_loc_cfg_01, art_loc_cfg_01, loc = st_confs
    store_handler = StoreHandler(metadata_store=md_loc_cfg_01, store=art_loc_cfg_01)
    return RunBuilder(store_handler), loc


class TestRunBuilder:
    def test_init_run(self, build_builder_local):
        bld, loc = build_builder_local
        bld._init_run("test", "test", True)
        path = Path(loc, "metadata", "test", "test")
        assert path.exists()
        assert path.is_dir()

    def test_get_md_uri(self, build_builder_local):
        bld, loc = build_builder_local
        uri = bld._get_md_uri("test", "test")
        assert uri == Path(loc, "metadata", "test", "test").as_posix()

    def test_get_art_uri(self, build_builder_local):
        bld, loc = build_builder_local
        uri = bld._get_art_uri("test", "test")
        assert uri == Path(loc, "artifact", "test", "test").as_posix()

    def test_check_unique_resource(self, build_builder_local):
        bld, _ = build_builder_local
        with pytest.raises(RunError):
            bld._check_unique_resource([RES_LOCAL_01, RES_LOCAL_01])

    def test_create_run(self, build_builder_local):
        bld, loc = build_builder_local
        run = bld.create_run([RES_LOCAL_01], RUN_CFG_EMPTY, "test", "test", True)
        path = Path(loc, "metadata", "test", "test")
        assert path.exists()
        assert path.is_dir()
        assert isinstance(run, Run)
