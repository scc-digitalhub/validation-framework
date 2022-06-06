"""
Configurations module for runs, stores and constraints.
"""
# pylint: disable=too-few-public-methods,import-error,missing-class-docstring
from typing import Any, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field
from typing_extensions import Literal
from datajudge.data.data_resource import DataResource

from datajudge.utils.commons import (AZURE, CHECK_ROWS, CHECK_VALUE, DUCKDB,
                                     DUMMY, EMPTY, EXACT, FRICTIONLESS, FRICTIONLESS_SCHEMA, FTP,
                                     HTTP, LOCAL, MAXIMUM, MINIMUM, NON_EMPTY,
                                     ODBC, RANGE, S3, SQL)


class StoreConfig(BaseModel):
    name: str
    type: Literal[LOCAL, HTTP, FTP, S3, AZURE, SQL, ODBC, DUMMY]
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


class ConstraintFullFrictionless(Constraint):
    type: Literal[FRICTIONLESS_SCHEMA]
    table_schema: dict


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


# Dummy generic configs
DUMMY_STORE = StoreConfig(name=DUMMY, type=DUMMY, uri=f"{DUMMY}://")
DUMMY_RES = DataResource(path=f"{DUMMY}://", name=DUMMY, store=DUMMY)
DUMMY_CONST = Constraint(name=DUMMY, title=DUMMY, resources=[DUMMY], weight=0)
