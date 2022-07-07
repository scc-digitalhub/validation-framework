"""
Configurations module for runs, stores and constraints.
"""
# pylint: disable=too-few-public-methods,import-error,missing-class-docstring
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

    Attributes
    ----------
    name : str
        Store id.
    type : str
        Store type to instantiate.
    uri : str
        Store URI.
    title : str, optional
        Human readable name for Store.
    isDefault : bool, optional
        Determine if a Store is the default one.
    config : dict, optional
        Dictionary containing the configuration for the backend.

    """
    name: str
    type: Literal[LOCAL, HTTP, FTP, S3, AZURE, SQL, ODBC, DUMMY]
    uri: str
    title: Optional[str] = None
    isDefault: Optional[bool] = False
    config: Optional[dict] = None


class Constraint(BaseModel):
    """
    Base model for constraint.
    """
    _id: str = Field(default_factory=uuid4)
    name: str
    title: str
    resources: List[str]
    weight: int


class ConstraintFrictionless(Constraint):
    """
    Frictionless contraint.
    
    Attributes
    ----------
    name : str
        Constraint id.
    title : str
        Human readable name for the constraint.
    resources : list
        List of resources affected by the constraint.
    weight : int
        Criticity of an eventual error encountered in the
        validation for the constraint.
    type : str = "frictionless"
        Constraint type (mandatory "frictionless").
    field : str
        Field to validate.
    fieldType : str
        Datatype of the field to validate.
    constraint : str
        Frictionless constraint typology.
    value : Any
        Value of the constraint.

    """
    type: Literal[FRICTIONLESS]
    field: str
    fieldType: str
    constraint: str
    value: Any


class ConstraintFullFrictionless(Constraint):
    """
    Frictionless full schema contraint.
    
    Attributes
    ----------
    name : str
        Constraint id.
    title : str
        Human readable name for the constraint.
    resources : list
        List of resources affected by the constraint.
    weight : int
        Criticity of an eventual error encountered in the
        validation for the constraint.
    type : str = "frictionless_schema"
        Constraint type (mandatory "frictionless_schema").
    table_schema : dict
        Table schema to validate a resource.

    """
    type: Literal[FRICTIONLESS_SCHEMA]
    table_schema: dict


class ConstraintDuckDB(Constraint):
    """
    DuckDB contraint.
    
    Attributes
    ----------
    name : str
        Constraint id.
    title : str
        Human readable name for the constraint.
    resources : list
        List of resources affected by the constraint.
    weight : int
        Criticity of an eventual error encountered in the
        validation for the constraint.
    type : str = "duckdb"
        Constraint type (mandatory "duckdb").
    query : str
        SQL query to execute over resources.
    expect : str
        SQL constraint type to check.
    value : Any
        Value of the constraint.
    check : str, optional
        Modality of constraint checking (On rows or single value).

    """
    type: Literal[DUCKDB]
    query: str
    expect: Literal[EMPTY, NON_EMPTY, EXACT, RANGE, MINIMUM, MAXIMUM]
    value: Optional[Any] = None
    check: Literal[CHECK_VALUE, CHECK_ROWS] = CHECK_ROWS


class ConstraintSqlAlchemy(Constraint):
    """
    SqlAlchemy contraint.
    
    Attributes
    ----------
    name : str
        Constraint id.
    title : str
        Human readable name for the constraint.
    resources : list
        List of resources affected by the constraint.
    weight : int
        Criticity of an eventual error encountered in the
        validation for the constraint.
    type : str = "sqlalchemy"
        Constraint type (mandatory "sqlalchemy").
    query : str
        SQL query to execute over resources.
    expect : str
        SQL constraint type to check.
    value : Any
        Value of the constraint.
    check : str, optional
        Modality of constraint checking (On rows or single value).

    """
    type: Literal[SQLALCHEMY]
    query: str
    expect: Literal[EMPTY, NON_EMPTY, EXACT, RANGE, MINIMUM, MAXIMUM]
    value: Optional[Any] = None
    check: Literal[CHECK_VALUE, CHECK_ROWS] = CHECK_ROWS


class ConstraintGreatExpectation(Constraint):
    """
    Great Expectation contraint.
    
    Attributes
    ----------
    name : str
        Constraint id.
    title : str
        Human readable name for the constraint.
    resources : list
        List of resources affected by the constraint.
    weight : int
        Criticity of an eventual error encountered in the
        validation for the constraint.
    type : str = "great_expectation"
        Constraint type (mandatory "great_expectation").
    expectation : str
        Name of the expectation to apply to data.
    expect : str
        Arguments for the exepectation.

    """
    type: Literal[GREAT_EXPECTATION]
    expectation: str
    expectation_args: dict


class ExecConfig(BaseModel):
    """
    Generic configuration for run operation.
    
    Attributes
    ----------
    library : str, optional
        Library to use for performing an operation.
    execArgs : dict, optional
        Execution arguments to pass to plugins.
    tmpFormat : str
        Specific format to fetch data from backend.

    """
    _id: str = Field(default_factory=uuid4)
    library: Optional[str] = DUMMY
    execArgs: Optional[dict] = {}
    tmpFormat: Optional[str] = "csv"


class RunConfig(BaseModel):
    """
    Run configuration object.
    
    Attributes
    ----------
    validation : List[ExecConfig], optional
        List of validation configuration.
    inference : List[ExecConfig], optional
        List of inference configuration.
    profiling : List[ExecConfig], optional
        List of profiling configuration.

    """
    validation: Optional[List[ExecConfig]] = [ExecConfig()]
    inference: Optional[List[ExecConfig]] = [ExecConfig()]
    profiling: Optional[List[ExecConfig]] = [ExecConfig()]


# Dummy generic configs
DUMMY_STORE = StoreConfig(name=DUMMY, type=DUMMY, uri=f"{DUMMY}://")
DUMMY_RES = DataResource(path=f"{DUMMY}://", name=DUMMY, store=DUMMY)
DUMMY_CONST = Constraint(name=DUMMY, title=DUMMY, resources=[DUMMY], weight=0)
