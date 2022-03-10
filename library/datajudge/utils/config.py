"""
Configuration for filenames, endpoints, etc.
"""
# pylint: disable=too-few-public-methods,import-error,missing-class-docstring
from typing import Any, List, Optional, Union
from typing_extensions import Literal

from pydantic import BaseModel


class StoreConfig(BaseModel):
    title: Optional[str] = None
    name: str
    path: str
    isDefault: bool = False
    config: Optional[dict] = None


class Constraint(BaseModel):
    name: str
    title: str
    resources: List[str]
    severity: int


class ConstraintsFrictionless(Constraint):
    type: Literal["frictionless"]
    field: str
    field_type: str
    constraint: str
    value: Any


class ConstraintsDatajudge(Constraint):
    type: Literal["datajudge"]
    query: str
    expect: str


class ExecutionConfig(BaseModel):
    enabled: bool = False
    library: Optional[Union[str, List[str]]] = None
    exec_args: Optional[dict] = None


class RunConfig(BaseModel):
    validation: Optional[ExecutionConfig] = ExecutionConfig()
    inference: Optional[ExecutionConfig] = ExecutionConfig()
    profiling: Optional[ExecutionConfig] = ExecutionConfig()
    snapshot: Optional[ExecutionConfig] = ExecutionConfig()


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
FN_DJ_REPORT = "report_{}.json"
FN_DJ_SCHEMA = "schema_{}.json"
FN_DJ_PROFILE = "profile_{}.json"
FN_ARTIFACT_METADATA = "artifact_metadata_{}.json"
FN_RUN_ENV = "run_env.json"

# Metadata type
MT_RUN_METADATA = "run"
MT_DJ_REPORT = "report"
MT_DJ_SCHEMA = "schema"
MT_DJ_PROFILE = "profile"
MT_ARTIFACT_METADATA = "artifact"
MT_RUN_ENV = "run_env"

# Execution operations
OP_INF = "inference"
OP_PRO = "profiling"
OP_VAL = "validation"
