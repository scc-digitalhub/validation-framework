"""
Configuration for filenames, endpoints, etc.
"""
# pylint: disable=too-few-public-methods,import-error,missing-class-docstring
from uuid import uuid4
from typing import Any, List, Optional
from typing_extensions import Literal

from pydantic import BaseModel, Field


class StoreConfig(BaseModel):
    name: str
    uri: str
    title: Optional[str] = None
    isDefault: bool = False
    config: Optional[dict] = None


class Constraint(BaseModel):
    _id: str = Field(default_factory=uuid4)
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


class ExecConfig(BaseModel):
    _id: str = Field(default_factory=uuid4)
    library: Optional[str] = "_dummy"
    exec_args: Optional[dict] = {}
    store_artifact: bool = False


class OpsConfig(BaseModel):
    enabled: bool = True
    config: Optional[List[ExecConfig]] = [ExecConfig()]


class RunConfig(BaseModel):
    validation: Optional[OpsConfig] = OpsConfig()
    inference: Optional[OpsConfig] = OpsConfig()
    profiling: Optional[OpsConfig] = OpsConfig()


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

# Execution status
STATUS_INIT = "created"
STATUS_RUNNING = "executing"
STATUS_INTERRUPTED = "interrupdted"
STATUS_FINISHED = "finished"
STATUS_ERROR = "error"
