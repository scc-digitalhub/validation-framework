"""
Configurations module for runs, stores and constraints.
"""
# pylint: disable=too-few-public-methods,import-error,missing-class-docstring
from typing import Any, List, Optional
from typing_extensions import Literal
from uuid import uuid4

from pydantic import BaseModel, Field

from datajudge.utils.commons import (DUCKDB, DUMMY, EMPTY, EXACT, FRICTIONLESS,
                                    NON_EMPTY, RANGE)


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
    type: Literal[FRICTIONLESS]
    field: str
    field_type: str
    constraint: str
    value: Any


class ConstraintsDuckDB(Constraint):
    type: Literal[DUCKDB]
    query: str
    expect: Literal[EMPTY, NON_EMPTY, EXACT, RANGE]
    value: Optional[Any] = None


class ExecConfig(BaseModel):
    _id: str = Field(default_factory=uuid4)
    library: Optional[str] = DUMMY
    exec_args: Optional[dict] = {}
    store_artifact: bool = False


class OpsConfig(BaseModel):
    enabled: bool = True
    config: Optional[List[ExecConfig]] = [ExecConfig()]


class RunConfig(BaseModel):
    validation: Optional[OpsConfig] = OpsConfig()
    inference: Optional[OpsConfig] = OpsConfig()
    profiling: Optional[OpsConfig] = OpsConfig()
