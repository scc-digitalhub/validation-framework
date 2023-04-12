import csv
import sqlite3
from tempfile import TemporaryDirectory

from datajudge.client.store_factory import StoreBuilder
from datajudge.client.store_handler import StoreHandler
from datajudge.plugins.utils.plugin_utils import Result
from datajudge.utils.config import DataResource, RunConfig, StoreConfig
from datajudge.utils.config import (
    ConstraintFrictionless,
    ConstraintFullFrictionless,
    RunConfig,
    StoreConfig,
    DataResource,
)


class Configurator:
    def __init__(self) -> None:
        """Create temp dir and store builder"""
        self.tmp = TemporaryDirectory()
        self.store_builder = StoreBuilder("test", self.tmp.name)

    def get_tmp(self):
        """Get temporary folder name"""
        return self.tmp.name

    def get_resource(self, cfg):
        """Return DataResource"""
        return DataResource(**cfg)

    def get_store_cfg(self, cfg, tmp=False):
        """Return StoreConfig"""
        cfg = StoreConfig(**cfg)
        if tmp:
            return self.up_tmp_store_cfg(cfg)
        return cfg

    def up_tmp_store_cfg(self, cfg):
        """Update URI in StoreConfig to temporary URI"""
        cfg.uri = self.get_tmp()
        return cfg

    def get_run_cfg(self, cfg):
        """Return RunConfig"""
        return RunConfig(**cfg)

    def get_store(self, cfg, tmp=False, md=False):
        """Build a store object"""
        if not isinstance(cfg, StoreConfig):
            cfg = self.get_store_cfg(cfg, tmp)
        return self.store_builder.build(cfg, md_store=md)

    def get_result_test(
        self, status="test", duration="test", errors="test", artifact="test"
    ):
        """Return a generic result object"""
        return Result(status, duration, errors, artifact)

    def destroy(self):
        """Cleanup of temp dir"""
        self.tmp.cleanup()


# Stores

METADATA_STORE_LOCAL = {
    "title": "Local Metadata Store",
    "name": "local_md",
    "type": "local",
    "uri": "./djruns",
}

STORE_LOCAL_01 = {
    "title": "Local Store",
    "name": "local",
    "type": "local",
    "uri": "./djruns",
    "isDefault": True,
}
STORE_LOCAL_02 = {
    "title": "Local Store 2",
    "name": "local_2",
    "type": "local",
    "uri": "./djruns",
    "isDefault": False,
}

# Resources

RES_LOCAL_01 = DataResource(
    path="tests/synthetic_data/test_csv_file.csv", name="res_test_01", store="local"
)

RES_LOCAL_02 = DataResource(
    path="tests/synthetic_data/test_csv_file_2.csv", name="res_test_02", store="local"
)

# Run

RUN_CFG_EMPTY = RunConfig()


# Constraints
# Frictionless

CONST_FRICT_01 = ConstraintFrictionless(
    title="Test frictionless constraint",
    name="test-const-frict-01",
    resources=["res_test_01"],
    field="col1",
    fieldType="string",
    constraint="maxLength",
    value=1,
    weight=5,
)

CONST_FRICT_02 = ConstraintFrictionless(
    title="Test frictionless constraint",
    name="test-const-frict-02",
    resources=["res_test_01"],
    field="col1",
    fieldType="string",
    constraint="minLength",
    value=5,
    weight=5,
)

CONST_FRICT_FULL_01 = ConstraintFullFrictionless(
    title="Test frictionless constraint",
    name="test-const-frict-01",
    resources=["res_test_01"],
    tableSchema={
        "fields": [
            {"name": "col1", "type": "string"},
            {"name": "col2", "type": "number"},
            {"name": "col3", "type": "integer"},
            {"name": "col4", "type": "date"},
        ]
    },
    weight=5,
)


# Utilities


def get_str_cfg(str_dict):
    return StoreConfig(**str_dict)


def set_tmp(store_cfg, tmp):
    store_cfg.uri = tmp
    return store_cfg


# Readapted from https://stackoverflow.com/a/2888042/13195227
def insert_in_db(path):
    data_path = "tests/synthetic_data/test_csv_file.csv"

    con = sqlite3.connect(path)
    cur = con.cursor()
    cur.execute("CREATE TABLE test (col1, col2, col3, col4);")

    with open(data_path, "r") as fin:
        dr = csv.DictReader(fin)
        to_db = [(i["col1"], i["col2"], i["col3"], i["col4"]) for i in dr]

    cur.executemany(
        "INSERT INTO test (col1, col2, col3, col4) VALUES (?, ?, ?, ?);", to_db
    )
    con.commit()
    con.close()
