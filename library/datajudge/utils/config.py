"""
Configuration for filenames, endpoints, etc.
"""
from typing import Any, List, Optional, Union
from pydantic import BaseModel, Field


class StoreConfig(BaseModel):
    title: Optional[str] = None
    name: str
    path: str
    isDefault: bool = False
    config: Optional[dict] = None


class FrictionlessConst(BaseModel):
    name: str
    schema_: dict = Field(alias="schema")


class DatajudgeConstList(BaseModel):
    title: str
    name: str
    query: str
    expect: str
    value: Optional[Any] = None
    errors: dict

       
class DatajudgeConst(BaseModel):
    name: str
    path: str
    constraintsList: List[DatajudgeConstList]

       
class ConstLib(BaseModel):
    frictionless: FrictionlessConst = None
    datajudge: List[DatajudgeConst] = None


class ValidationConfig(BaseModel):
    enabled: bool = False
    library: Optional[str] = None


class InferenceConfig(BaseModel):
    enabled: bool = False
    library: Optional[str] = None


class ProfilingConfig(BaseModel):
    enabled: bool = False
    library: Optional[str] = None


class SnapshotConfig(BaseModel):
    enabled: bool = False
    library: Optional[str] = None


Configs = Union[ValidationConfig,
                InferenceConfig,
                ProfilingConfig,
                SnapshotConfig]


class RunConfig(BaseModel):

    # validation: Optional[List[ValidationConfig]] = ValidationConfig()
    # inference: Optional[List[InferenceConfig]] = InferenceConfig()
    # profiling: Optional[List[ProfilingConfig]] = ProfilingConfig()
    # snapshot: Optional[List[SnapshotConfig]] = SnapshotConfig()
    validation: Optional[ValidationConfig] = ValidationConfig()
    inference: Optional[InferenceConfig] = InferenceConfig()
    profiling: Optional[ProfilingConfig] = ProfilingConfig()
    snapshot: Optional[SnapshotConfig] = SnapshotConfig()


# DATAJUDGE VERSION
DATAJUDGE_VERSION = "1.1.0"

# FILENAMES METADATA
FN_RUN_METADATA = "run_metadata.json"
FN_DATA_RESOURCE = "data_resource.json"
FN_DJ_REPORT = "report.json"
FN_DJ_SCHEMA = "schema.json"
FN_DJ_PROFILE = "profile.json"
FN_ARTIFACT_METADATA = "artifact_metadata_{}.json"
FN_RUN_ENV = "run_env.json"

# FILENAMES ARTIFACTS
FN_VALID_SCHEMA = "table_schema.json"
FN_FULL_REPORT = "report.json"
FN_INFERRED_SCHEMA = "schema.json"

# API ENDPOINTS
API_BASE = "/api/project/"
API_RUN_METADATA = "/run-metadata"
API_DATA_RESOURCE = "/data-resource"
API_DJ_REPORT = "/short-report"
API_DJ_SCHEMA = "/short-schema"
API_DJ_PROFILE = "/data-profile"
API_ARTIFACT_METADATA = "/artifact-metadata"
API_RUN_ENV = "/run-environment"

# METADATA TYPE
MT_RUN_METADATA = "run"
MT_DATA_RESOURCE = "resource"
MT_DJ_REPORT = "report"
MT_DJ_SCHEMA = "schema"
MT_DJ_PROFILE = "profile"
MT_ARTIFACT_METADATA = "artifact"
MT_RUN_ENV = "run_env"

# DEFAULT FOLDERS/STORES
DEFAULT_LOCAL = "./djruns"
DEFAULT_TMP = DEFAULT_LOCAL + "/tmp"
DEFAULT_STORE = StoreConfig(title="Local Default Store",
                            name="local",
                            path=DEFAULT_LOCAL,
                            isDefault=True)
DEFAULT_MD_STORE = StoreConfig(title="Local Metadata Store",
                               name="local_md",
                               path=DEFAULT_LOCAL)

# DEFAULT NAMES
DEFAULT_PROJ = "project"
DEFAULT_EXP = "experiment"
