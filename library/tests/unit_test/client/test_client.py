import pytest

from datajudge.client.client import Client
from datajudge.run.run import Run
from datajudge.utils.exceptions import StoreError


class TestClient:
    def test_create_empty_client(self):
        client = Client()
        assert isinstance(client, Client)

    def test_create_client_only_metadata_store(self, mds_cfg):
        client = Client(metadata_store=mds_cfg)
        assert isinstance(client, Client)

    def test_create_client_only_artifact_store(self, st_loc1):
        client = Client(store=st_loc1)
        assert isinstance(client, Client)

    def test_create_client(self, st_loc1, mds_cfg):
        client = Client(metadata_store=mds_cfg, store=st_loc1)
        assert isinstance(client, Client)

    def test_create_client_multiple_stores(self, st_loc1, st_loc2, mds_cfg):
        client = Client(
            metadata_store=mds_cfg,
            store=[st_loc1, st_loc2],
        )
        assert isinstance(client, Client)

    def test_add_store(self, st_loc1, st_loc2, mds_cfg):
        client = Client(metadata_store=mds_cfg, store=[st_loc1])
        client.add_store(st_loc2)

    def test_add_same_store(self, st_loc1, mds_cfg):
        client = Client(metadata_store=mds_cfg, store=[st_loc1])
        with pytest.raises(StoreError):
            client.add_store(st_loc1)

    def test_fail_add_store(self):
        client = Client()
        with pytest.raises(TypeError):
            client.add_store([])

    def test_create_run(self, st_loc1, mds_cfg, run_empty, local_resource):
        client = Client(metadata_store=mds_cfg, store=[st_loc1])
        run = client.create_run([local_resource], run_empty)
        assert isinstance(run, Run)


# Metadata store config
@pytest.fixture
def mds_cfg(local_md_store_cfg):
    return local_md_store_cfg


# Artifact store config 1
@pytest.fixture
def st_loc1(local_store_cfg):
    return local_store_cfg


# Artifact store config 2
@pytest.fixture
def st_loc2(local_store_cfg_2):
    return local_store_cfg_2
