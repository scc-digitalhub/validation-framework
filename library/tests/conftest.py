import csv
import os
import sqlite3
import shutil
from io import StringIO, BytesIO
from unittest.mock import MagicMock

import boto3
import duckdb
import pytest
from moto import mock_s3

from datajudge.client.store_factory import StoreBuilder
from datajudge.data_reader.utils import build_reader
from datajudge.plugins.utils.plugin_utils import Result
from datajudge.utils.config import (
    ConstraintFrictionless,
    ConstraintFullFrictionless,
    ConstraintGreatExpectations,
    ConstraintSqlAlchemy,
    ConstraintDuckDB,
    DataResource,
    RunConfig,
    StoreConfig,
)
from datajudge.utils.commons import *
from datajudge.utils.utils import listify


##############################
# DATA
##############################


# Tmp root
@pytest.fixture(scope="session")
def temp_folder(tmp_path_factory):
    return tmp_path_factory.mktemp("data")


@pytest.fixture(scope="session")
def temp_data(temp_folder):
    return str(temp_folder)


# Sample csv
@pytest.fixture(scope="session")
def data_path_csv(temp_folder):
    tmp = str(temp_folder / "test_csv_file.csv")
    shutil.copy("tests/synthetic_data/test_csv_file.csv", tmp)
    return tmp


# Sample parquet
@pytest.fixture(scope="session")
def data_path_parquet(temp_folder):
    tmp = str(temp_folder / "test_parquet_file.parquet")
    shutil.copy("tests/synthetic_data/test_parquet_file.parquet", tmp)
    return tmp


# Sample sqlite database
# Readapted from https://stackoverflow.com/a/2888042/13195227
@pytest.fixture(scope="session")
def sqlitedb(temp_folder, data_path_csv):
    tmp = str(temp_folder / "test.db")
    con = sqlite3.connect(tmp)
    cur = con.cursor()
    cur.execute("CREATE TABLE test (col1, col2, col3, col4);")
    with open(data_path_csv, "r") as fin:
        dr = csv.DictReader(fin)
        to_db = [(i["col1"], i["col2"], i["col3"], i["col4"]) for i in dr]
    cur.executemany(
        "INSERT INTO test (col1, col2, col3, col4) VALUES (?, ?, ?, ?);", to_db
    )
    con.commit()
    con.close()
    return f"sqlite:///{tmp}"


# Sample duckdb database
@pytest.fixture(scope="session")
def tmpduckdb(temp_folder, data_path_csv):
    tmp = str(temp_folder / "duckdb.db")
    con = duckdb.connect(tmp)
    sql = f"CREATE TABLE test AS SELECT * FROM read_csv_auto('{data_path_csv}');"
    con.execute(sql)
    con.close()
    return tmp


# Saample Result object
@pytest.fixture(scope="session")
def result_obj():
    return Result("test", "test", "test", "test")


# Temporary file
@pytest.fixture(scope="session")
def temp_file(temp_folder):
    file = temp_folder / "test.txt"
    file.write_text("test")
    return file


# StringIO sample
@pytest.fixture
def stringio():
    io = StringIO()
    io.write("test")
    io.seek(0)
    return io


# BytesIO sample
@pytest.fixture
def bytesio():
    io = BytesIO()
    io.write(b"test")
    io.seek(0)
    return io


# Dict sample
@pytest.fixture
def dictionary():
    return {"a": 1, "b": 2}


##############################
# FIXTURES & CONFIGS
##############################

# ---------------
# RUNS
# ---------------


@pytest.fixture
def run_empty():
    return RunConfig()


# ---------------
# STORES
# ---------------


@pytest.fixture(scope="session")
def store_builder(temp_folder):
    return StoreBuilder("test", temp_folder)


@pytest.fixture
def store(store_cfg, store_builder):
    return store_builder.build(store_cfg)


# ---------------
# Artifact Stores
# ---------------


# Local 1
@pytest.fixture
def local_store_cfg(temp_data):
    return StoreConfig(
        **{
            "title": "Local Store",
            "name": "local",
            "type": "local",
            "uri": temp_data,
            "isDefault": True,
        }
    )


# Local 2
@pytest.fixture
def local_store_cfg_2():
    return StoreConfig(
        **{
            "title": "Local Store 2",
            "name": "local_2",
            "type": "local",
            "uri": "./djruns",
            "isDefault": False,
        }
    )


# SQL
@pytest.fixture
def sql_store_cfg(sqlitedb):
    return StoreConfig(
        **{
            "title": "SQLite Store",
            "name": "sql",
            "type": "sql",
            "uri": "sql://test",
            "isDefault": True,
            "config": {"connection_string": sqlitedb},
        }
    )


# S3
@pytest.fixture
def s3_store_cfg():
    return StoreConfig(
        **{
            "title": "S3 Store",
            "name": "s3",
            "type": "s3",
            "uri": "s3://test",
            "isDefault": True,
            "config": {
                "aws_access_key_id": "test",
                "aws_secret_access_key": "test",
                "endpoint_url": "http://localhost:9000/",
            },
        }
    )


# ----------------
# Metadata Stores
# ----------------


# Local
@pytest.fixture
def local_md_store_cfg(temp_data):
    return StoreConfig(
        **{
            "title": "Local Metadata Store",
            "name": "local_md",
            "type": "local",
            "uri": temp_data,
        }
    )


# ----------------
# DATA READER
# ----------------


@pytest.fixture
def reader(data_reader, store):
    return build_reader(data_reader, store)


# ----------------
# DATA RESOURCES
# ----------------


@pytest.fixture
def local_resource(data_path_csv):
    return DataResource(path=data_path_csv, name="res_test_01", store="local")


@pytest.fixture
def local_resource_no_temp():
    return DataResource(
        path="tests/synthetic_data/test_csv_file.csv", name="res_test_01", store="local"
    )


@pytest.fixture
def local_resource_2():
    return DataResource(
        path="tests/synthetic_data/test_csv_file_2.csv",
        name="res_test_02",
        store="local",
    )


@pytest.fixture
def sql_resource(sqlitedb):
    return DataResource(path=sqlitedb, name="res_test_01", store="sql")


# ----------------
# CONSTRAINTS
# ----------------

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
CONST_GE_01 = ConstraintGreatExpectations(
    name="const-ge-01",
    title="Test GE constraint",
    resources=["res_test_01"],
    expectation="expect_column_value_lengths_to_be_between",
    expectation_args={"column": "col1", "min_value": 1, "max_value": 1},
    weight=5,
)
CONST_SQLALCHEMY_01 = ConstraintSqlAlchemy(
    name="const-sqlalc-01",
    title="Test sqlalchemy constraint",
    resources=["res_test_01"],
    query="select * from test",
    expect="non-empty",
    check="rows",
    weight=5,
)
CONST_DUCKDB_01 = ConstraintDuckDB(
    name="const-duckdb-01",
    title="Test duckdb constraint",
    resources=["res_test_01"],
    query="select * from test",
    expect="non-empty",
    check="rows",
    weight=5,
)


# ----------------
# PLUGINS BUILDERS
# ----------------


@pytest.fixture
def config_plugin_builder(store):
    stores = listify(store)
    return {"stores": stores, "exec_args": {}}


@pytest.fixture
def plugin_builder_val_args(resource, constraint, error_report):
    resources = listify(resource)
    constraints = listify(constraint)
    return [resources, constraints, error_report]


@pytest.fixture
def plugin_builder_non_val_args(resource):
    resources = listify(resource)
    return [resources]


# ----------------
# PLUGINS
# ----------------


@pytest.fixture
def setted_plugin(plugin, config_plugin):
    plg = plugin()
    plg.setup(*config_plugin)
    return plg


@pytest.fixture(params=["partial", "full", "count"])
def error_report(request):
    return request.param


##############################
# MOCKS
##############################

# ----------------
# Factory
# ----------------


def mock_object_factory(**kwargs):
    mock_obj = MagicMock()
    for k, v in kwargs.items():
        setattr(mock_obj, k, v)
    return mock_obj


# ----------------
# Mock constraints
# ----------------

mock_c_frict = mock_object_factory(type=LIBRARY_FRICTIONLESS)
mock_c_frict_full = mock_object_factory(type=CONSTRAINT_FRICTIONLESS_SCHEMA)
mock_c_duckdb = mock_object_factory(type=LIBRARY_DUCKDB)
mock_c_gex = mock_object_factory(type=LIBRARY_GREAT_EXPECTATIONS)
mock_c_sqlalc = mock_object_factory(type=LIBRARY_SQLALCHEMY)

# ----------------
# Generic mock objects (c = constraint, r = resources, s = store)
# ----------------

mock_c_generic = mock_object_factory(type="generic", resources=["resource"])
mock_r_generic = mock_object_factory(name="resource", store="store")
mock_s_generic = mock_object_factory(name="store", type="generic")
mock_c_to_fail = mock_object_factory(type="generic", resources=["resource_fail"])
mock_r_to_fail = mock_object_factory(name="resource_fail", store="fail")
mock_s_to_fail = mock_object_factory(name="fail", type="fail")


# ----------------
# Mock plugins
# ----------------

S3_BUCKET = "test"


@pytest.fixture(scope="session")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["MOTO_S3_CUSTOM_ENDPOINTS"] = "http://localhost:9000"


@pytest.fixture(scope="session")
def s3(aws_credentials):
    with mock_s3():
        client = boto3.client("s3", region_name="us-east-1")
        client.create_bucket(Bucket=S3_BUCKET)
        client.upload_file(
            "tests/synthetic_data/test_csv_file.csv", S3_BUCKET, "test_csv_file.csv"
        )
        yield client

