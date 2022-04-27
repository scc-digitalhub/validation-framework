"""
Configurations module for runs, stores and constraints.
"""
# pylint: disable=too-few-public-methods,import-error,missing-class-docstring
from typing import Any, List, Optional
from typing_extensions import Literal
from uuid import uuid4

from pydantic import BaseModel, Field

from datajudge.utils.commons import (DUCKDB, DUMMY, FRICTIONLESS,
                                     EMPTY, NON_EMPTY, EXACT,
                                     RANGE, MINIMUM, MAXIMUM,
                                     CHECK_VALUE, CHECK_ROWS)


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
    weight: int


class ConstraintsFrictionless(Constraint):
    type: Literal[FRICTIONLESS]
    field: str
    fieldType: str
    constraint: str
    value: Any


class ConstraintsDuckDB(Constraint):
    type: Literal[DUCKDB]
    query: str
    expect: Literal[EMPTY, NON_EMPTY, EXACT, RANGE, MINIMUM, MAXIMUM]
    value: Optional[Any] = None
    check: Literal[CHECK_VALUE, CHECK_ROWS] = CHECK_ROWS


class ExecConfig(BaseModel):
    _id: str = Field(default_factory=uuid4)
    library: Optional[str] = DUMMY
    execArgs: Optional[dict] = {}
    storeArtifact: bool = False
    tmpFormat: Optional[str] = "csv"


class RunConfig(BaseModel):
    validation: Optional[List[ExecConfig]] = [ExecConfig()]
    inference: Optional[List[ExecConfig]] = [ExecConfig()]
    profiling: Optional[List[ExecConfig]] = [ExecConfig()]
