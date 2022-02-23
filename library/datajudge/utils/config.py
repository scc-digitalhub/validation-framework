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
    library: Optional[Union[str, List[str]]] = None


class InferenceConfig(BaseModel):
    enabled: bool = False
    library: Optional[Union[str, List[str]]] = None


class ProfilingConfig(BaseModel):
    enabled: bool = False
    library: Optional[Union[str, List[str]]] = None


class SnapshotConfig(BaseModel):
    enabled: bool = False
    library: Optional[Union[str, List[str]]] = None


class RunConfig(BaseModel):
    validation: Optional[ValidationConfig] = ValidationConfig()
    inference: Optional[InferenceConfig] = InferenceConfig()
    profiling: Optional[ProfilingConfig] = ProfilingConfig()
    snapshot: Optional[SnapshotConfig] = SnapshotConfig()


# Datajudge version
DATAJUDGE_VERSION = "1.1.0"

# API endpoints
API_BASE = "/api/project/"
API_RUN_METADATA = "/run-metadata"
API_DJ_REPORT = "/short-report"
API_DJ_SCHEMA = "/short-schema"
API_DJ_PROFILE = "/data-profile"
API_ARTIFACT_METADATA = "/artifact-metadata"
API_RUN_ENV = "/run-environment"

# Filenames metadata
FN_RUN_METADATA = "run_metadata.json"
FN_DJ_REPORT = "report.json"
FN_DJ_SCHEMA = "schema.json"
FN_DJ_PROFILE = "profile.json"
FN_ARTIFACT_METADATA = "artifact_metadata_{}.json"
FN_RUN_ENV = "run_env.json"

# Metadata type
MT_RUN_METADATA = "run"
MT_DJ_REPORT = "report"
MT_DJ_SCHEMA = "schema"
MT_DJ_PROFILE = "profile"
MT_ARTIFACT_METADATA = "artifact"
MT_RUN_ENV = "run_env"
