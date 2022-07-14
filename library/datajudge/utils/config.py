"""
Configurations module for runs, stores and constraints.
"""

from typing import Any, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field
from typing_extensions import Literal

from datajudge.data import DataResource
from datajudge.utils.commons import (AZURE, CHECK_ROWS, CHECK_VALUE, DUCKDB,
                                     DUMMY, EMPTY, EXACT, FRICTIONLESS,
                                     FRICTIONLESS_SCHEMA, FTP, GREAT_EXPECTATION, HTTP, LOCAL,
                                     MAXIMUM, MINIMUM, NON_EMPTY, ODBC, RANGE,
                                     S3, SQL, SQLALCHEMY)


class StoreConfig(BaseModel):
    """
    Store configuration class.
    This object define the configuration of a Store passed to a
    Client in order to create a Store object to interact with
    various backend storages.
    """
    name: str
    """Store id."""

    type: Literal[LOCAL, HTTP, FTP, S3, AZURE, SQL, ODBC, DUMMY]
    """Store type to instantiate."""

    uri: str
    """Store URI."""

    title: Optional[str] = None
    """Human readable name for Store."""

    isDefault: Optional[bool] = False
    """Determine if a Store is the default one."""

    config: Optional[dict] = None
    """Dictionary containing the configuration for the backend."""


class Constraint(BaseModel):
    """
    Base model for constraint.
    """
    _id: str = Field(default_factory=uuid4)
    name: str
    """Constraint id."""

    title: str
    """Human readable name for the constraint."""

    resources: List[str]
    """List of resources affected by the constraint."""

    weight: int
    """Criticity of an eventual error encountered in the validation for the constraint."""


class ConstraintFrictionless(Constraint):
    """
    Frictionless constraint.
    """
    type: str = Field(FRICTIONLESS, const=True)
    """Constraint type ("frictionless")."""

    field: str
    """Field to validate."""

    fieldType: str
    """Datatype of the field to validate."""

    constraint: str
    """Frictionless constraint typology."""

    value: Any
    """Value of the constraint."""


class ConstraintFullFrictionless(Constraint):
    """
    Frictionless full schema constraint.
    """
    type: str = Field(FRICTIONLESS_SCHEMA, const=True)
    """Constraint type ("frictionless_schema")."""

    table_schema: dict
    """Table schema to validate a resource."""


class ConstraintDuckDB(Constraint):
    """
    DuckDB constraint.
    """
    type: str = Field(DUCKDB, const=True)
    """Constraint type ("duckdb")."""

    query: str
    """SQL query to execute over resources."""

    expect: Literal[EMPTY, NON_EMPTY, EXACT, RANGE, MINIMUM, MAXIMUM]
    """SQL constraint type to check."""

    value: Optional[Any] = None
    """Value of the constraint."""

    check: Literal[CHECK_VALUE, CHECK_ROWS] = CHECK_ROWS
    """Modality of constraint checking (On rows or single value)."""


class ConstraintSqlAlchemy(Constraint):
    """
    SqlAlchemy constraint.
    """
    type: str = Field(SQLALCHEMY, const=True)
    """Constraint type ("sqlalchemy")."""

    query: str
    """SQL query to execute over resources."""

    expect: Literal[EMPTY, NON_EMPTY, EXACT, RANGE, MINIMUM, MAXIMUM]
    """SQL constraint type to check."""

    value: Optional[Any] = None
    """Value of the constraint."""

    check: Literal[CHECK_VALUE, CHECK_ROWS] = CHECK_ROWS
    """Modality of constraint checking (On rows or single value)."""


class ConstraintGreatExpectation(Constraint):
    """
    Great Expectation constraint.
    """
    type: str = Field(GREAT_EXPECTATION, const=True)
    """Constraint type ("great_expectation")."""

    expectation: str
    """Name of the expectation to apply to data."""

    expectation_args: dict
    """Arguments for the exepectation."""


class ExecConfig(BaseModel):
    """
    Generic configuration for run operation.
    """
    _id: str = Field(default_factory=uuid4)
    library: Optional[str] = DUMMY
    """Library to use for performing an operation."""

    execArgs: Optional[dict] = {}
    """Execution arguments to pass to plugins."""

    tmpFormat: Optional[str] = "csv"
    """Specific format to fetch data from backend."""


class RunConfig(BaseModel):
    """
    Run configuration object.
    """
    validation: Optional[List[ExecConfig]] = [ExecConfig()]
    """List of validation configuration."""

    inference: Optional[List[ExecConfig]] = [ExecConfig()]
    """List of inference configuration."""

    profiling: Optional[List[ExecConfig]] = [ExecConfig()]
    """List of profiling configuration."""


# Dummy generic configs
DUMMY_STORE = StoreConfig(name=DUMMY, type=DUMMY, uri=f"{DUMMY}://")
DUMMY_RES = DataResource(path=f"{DUMMY}://", name=DUMMY, store=DUMMY)
DUMMY_CONST = Constraint(name=DUMMY, title=DUMMY, resources=[DUMMY], weight=0)
