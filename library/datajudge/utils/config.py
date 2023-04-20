"""
Configurations module for runs, stores and constraints.
"""

from typing import Any, List, Optional, Union
from uuid import uuid4

from pydantic import BaseModel, Field, root_validator
from typing_extensions import Literal

from datajudge.utils.commons import (
    CONSTRAINT_FRICTIONLESS_SCHEMA,
    CONSTRAINT_SQL_CHECK_ROWS,
    CONSTRAINT_SQL_CHECK_VALUE,
    CONSTRAINT_SQL_EMPTY,
    CONSTRAINT_SQL_EXACT,
    CONSTRAINT_SQL_MAXIMUM,
    CONSTRAINT_SQL_MINIMUM,
    CONSTRAINT_SQL_NON_EMPTY,
    CONSTRAINT_SQL_RANGE,
    LIBRARY_DUCKDB,
    LIBRARY_DUMMY,
    LIBRARY_FRICTIONLESS,
    LIBRARY_GREAT_EXPECTATIONS,
    LIBRARY_SQLALCHEMY,
    STORE_AZURE,
    STORE_DUMMY,
    STORE_FTP,
    STORE_HTTP,
    STORE_LOCAL,
    STORE_ODBC,
    STORE_S3,
    STORE_SQL,
)


class StoreConfig(BaseModel):
    """
    Store configuration class.
    This object define the configuration of a Store passed to a
    Client in order to create a Store object to interact with
    various backend storages.
    """

    name: str
    """Store id."""

    type: Literal[
        STORE_LOCAL,
        STORE_HTTP,
        STORE_FTP,
        STORE_S3,
        STORE_AZURE,
        STORE_SQL,
        STORE_ODBC,
        STORE_DUMMY,
    ]
    """Store type to instantiate."""

    uri: str
    """Store URI."""

    title: Optional[str] = None
    """Human readable name for Store."""

    isDefault: Optional[bool] = False
    """Determine if a Store is the default one."""

    config: Optional[dict] = None
    """Dictionary containing the configuration for the backend."""


class DataResource(BaseModel):
    """
    Resource configuration class.
    This object represents a physical resource present
    on a backend or a virtual resource rebuildable starting
    from other resources.
    """

    _id: str = Field(default_factory=uuid4)
    """UUID of DataResource."""

    name: str
    """Name of the DataResource."""

    path: Union[str, List[str]]
    """An URI (or a list of URI) that point to data."""

    store: str
    """Store name where to find the resource."""

    package: Optional[str] = None
    """Package name that DataResource belongs to."""

    title: Optional[str] = None
    """Human readable name for the DataResource."""

    description: Optional[str] = None
    """A description of the DataResource."""

    tableSchema: Optional[Union[str, dict]] = None
    """Resource table schema or path to table schema."""


class Constraint(BaseModel):
    """
    Base model for constraint.
    """

    _id: str = Field(default_factory=uuid4)
    """UUID of constraint."""

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

    type: str = Field(LIBRARY_FRICTIONLESS, const=True)
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

    type: str = Field(CONSTRAINT_FRICTIONLESS_SCHEMA, const=True)
    """Constraint type ("frictionless_schema")."""

    tableSchema: dict
    """Table schema to validate a resource."""


class ConstraintBaseSQL(Constraint):
    query: str
    """SQL query to execute over resources."""

    expect: Literal[
        CONSTRAINT_SQL_EMPTY,
        CONSTRAINT_SQL_NON_EMPTY,
        CONSTRAINT_SQL_EXACT,
        CONSTRAINT_SQL_RANGE,
        CONSTRAINT_SQL_MINIMUM,
        CONSTRAINT_SQL_MAXIMUM,
    ]
    """SQL constraint type to check."""

    value: Optional[Any] = None
    """Value of the constraint."""

    check: Literal[
        CONSTRAINT_SQL_CHECK_VALUE,
        CONSTRAINT_SQL_CHECK_ROWS,
    ] = CONSTRAINT_SQL_CHECK_ROWS
    """Modality of constraint checking (On rows or single value)."""

    @root_validator
    def check_for_emptiness(cls, values):
        """
        Check that evaluation of emptiness is performed
        only at rows level.
        """
        check = values.get("check")
        expect = values.get("expect")
        if (
            expect in (CONSTRAINT_SQL_EMPTY, CONSTRAINT_SQL_NON_EMPTY)
            and check != CONSTRAINT_SQL_CHECK_ROWS
        ):
            raise ValueError("Invalid, check emptiness only on 'rows'.")
        return values


class ConstraintDuckDB(ConstraintBaseSQL):
    """
    DuckDB constraint.
    """

    type: str = Field(LIBRARY_DUCKDB, const=True)
    """Constraint type ("duckdb")."""


class ConstraintSqlAlchemy(ConstraintBaseSQL):
    """
    SqlAlchemy constraint.
    """

    type: str = Field(LIBRARY_SQLALCHEMY, const=True)
    """Constraint type ("sqlalchemy")."""


class ConstraintGreatExpectations(Constraint):
    """
    Great Expectation constraint.
    """

    type: str = Field(LIBRARY_GREAT_EXPECTATIONS, const=True)
    """Constraint type ("great_expectations")."""

    expectation: str
    """Name of the expectation to apply to data."""

    expectation_args: dict
    """Arguments for the exepectation."""


class ExecConfig(BaseModel):
    """
    Generic configuration for run operation.
    """

    _id: str = Field(default_factory=uuid4)
    """UUID of operation."""

    library: Optional[str] = LIBRARY_DUMMY
    """Library to use for performing an operation."""

    execArgs: Optional[dict] = {}
    """Execution arguments to pass to plugins."""


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
