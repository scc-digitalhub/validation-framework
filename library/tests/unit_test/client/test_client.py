import pytest

from datajudge.client.client import Client
from datajudge.run.run import Run
from datajudge.utils.exceptions import StoreError
from tests.conftest import (
    METADATA_STORE_LOCAL,
    RES_LOCAL_01,
    RUN_CFG_EMPTY,
    STORE_LOCAL_01,
    STORE_LOCAL_02,
    Configurator,
)


@pytest.fixture()
def st_confs() -> None:
    conf = Configurator()
    md_loc_cfg_01 = conf.get_store_cfg(METADATA_STORE_LOCAL, tmp=True)
    art_loc_cfg_01 = conf.get_store_cfg(STORE_LOCAL_01, tmp=True)
    return md_loc_cfg_01, art_loc_cfg_01


class TestClient:
    def test_create_empty_client(self):
        client = Client()
        assert isinstance(client, Client)

    def test_create_client_only_metadata_store(self, st_confs):
        md_loc_cfg_01, _ = st_confs
        client = Client(metadata_store=md_loc_cfg_01)
        assert isinstance(client, Client)

    def test_create_client_only_artifact_store(self, st_confs):
        _, art_loc_cfg_01 = st_confs
        client = Client(store=art_loc_cfg_01)
        assert isinstance(client, Client)

    def test_create_client(self, st_confs):
        md_loc_cfg_01, art_loc_cfg_01 = st_confs
        client = Client(metadata_store=md_loc_cfg_01, store=art_loc_cfg_01)
        assert isinstance(client, Client)

    def test_create_client_multiple_stores(self, st_confs):
        md_loc_cfg_01, art_loc_cfg_01 = st_confs
        client = Client(
            metadata_store=md_loc_cfg_01,
            store=[art_loc_cfg_01, STORE_LOCAL_02],
        )
        assert isinstance(client, Client)

    def test_add_store(self, st_confs):
        md_loc_cfg_01, art_loc_cfg_01 = st_confs
        client = Client(metadata_store=md_loc_cfg_01, store=[art_loc_cfg_01])
        client.add_store(STORE_LOCAL_02)

    def test_add_same_store(self, st_confs):
        md_loc_cfg_01, art_loc_cfg_01 = st_confs
        client = Client(metadata_store=md_loc_cfg_01, store=[art_loc_cfg_01])
        with pytest.raises(StoreError):
            client.add_store(art_loc_cfg_01)

    def test_fail_add_store(self):
        client = Client()
        with pytest.raises(TypeError):
            client.add_store([])

    def test_create_run(self, st_confs):
        md_loc_cfg_01, art_loc_cfg_01 = st_confs
        client = Client(metadata_store=md_loc_cfg_01, store=[art_loc_cfg_01])
        run = client.create_run([RES_LOCAL_01], RUN_CFG_EMPTY)
        assert isinstance(run, Run)
