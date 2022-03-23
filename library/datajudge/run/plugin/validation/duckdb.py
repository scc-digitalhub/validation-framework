"""
Frictionless implementation of validation plugin.
"""
# pylint: disable=import-error,no-name-in-module,arguments-differ,no-member,too-few-public-methods
from __future__ import annotations

import typing
from typing import Any, List, Tuple

import duckdb
import pandas as pd

from datajudge.data.datajudge_report import DatajudgeReport
from datajudge.run.plugin.base_plugin import PluginBuilder
from datajudge.run.plugin.validation.validation_plugin import (
    Validation)
from datajudge.utils.commons import DUCKDB, EMPTY, EXACT, NON_EMPTY, RANGE
from datajudge.run.plugin.plugin_utils import exec_decorator
from datajudge.utils.utils import flatten_list

if typing.TYPE_CHECKING:
    from datajudge.data.data_resource import DataResource
    from datajudge.utils.config import Constraint, ConstraintsDuckDB
    from datajudge.run.plugin.base_plugin import Result


class ValidationPluginDuckDB(Validation):
    """
    DuckDB implementation of validation plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.connection = None
        self.constraint = None
        self.exec_args = None

    def setup(self,
              connection: duckdb.DuckDBPyConnection,
              constraint: ConstraintsDuckDB,
              exec_args: dict) -> None:
        """
        Set plugin resource.
        """
        self.connection = connection
        self.constraint = constraint
        self.exec_args = exec_args

    @exec_decorator
    def validate(self) -> dict:
        """
        Validate a Data Resource.
        """
        self.connection.execute(self.constraint.query)
        result = self.connection.fetchdf()
        valid, error = self.check_valid(result,
                                        self.constraint.expect,
                                        self.constraint.value)
        return {
            "result": result.to_dict(),
            "valid": valid,
            "error": error
        }

    @staticmethod
    def check_valid(result: pd.DataFrame,
                    expect: str,
                    value: Any) -> Tuple[bool, list]:
        """
        Parse query result accordigly to expected result.
        """
        if expect == EMPTY:
            valid = result.empty
            error = ("Table is not empty")
        elif expect == NON_EMPTY:
            valid = not result.empty
            error = ("Table is empty")
        elif expect == EXACT:
            try:
                res_val = result.iloc[0, 0]
                valid = bool(res_val == value)
                error = (f"Expected value {value}, instead got {res_val}")
            except:
                valid = False
                error = (f"Expected value {value}, but something went wrong")
        elif expect == RANGE:
            raise NotImplementedError
        else:
            raise NotImplementedError

        if valid:
            return valid, None
        return valid, error

    @exec_decorator
    def render_datajudge(self, result: Result) -> DatajudgeReport:
        """
        Return a DatajudgeReport.
        """
        constraint = self.constraint.dict()
        duration = result.duration
        valid = result.artifact.get("valid")
        errors = result.artifact.get("error")
        return DatajudgeReport(self.get_lib_name(),
                               self.get_lib_version(),
                               duration,
                               constraint,
                               valid,
                               errors)

    @exec_decorator
    def render_artifact(self, result: Result) -> List[tuple]:
        """
        Return a rendered report ready to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"error": result.errors}
        else:
            _object = dict(result.artifact)
        filename = self._fn_report.format(f"{DUCKDB}.json")
        artifacts.append(self.get_render_tuple(_object, filename))
        return artifacts

    @staticmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """
        return duckdb.__name__

    @staticmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """
        return duckdb.__version__


class ValidationBuilderDuckDB(PluginBuilder):
    """
    Validation plugin builder.
    """
    def build(self,
              resources: List[DataResource],
              constraints: List[Constraint]) -> ValidationPluginDuckDB:
        """
        Build a plugin for every resource and every constraint.
        """
        
        self.setup()
        
        # Filter resource used
        res_names = set(flatten_list(
                            [const.resources for const in constraints if 
                                const.type == "duckdb"]))
        res_to_register = [res for res in resources if res.name in res_names]
        self.register_resources(res_to_register)

        plugins = []
        for const in constraints:
            if const.type == "duckdb":
                plugin = ValidationPluginDuckDB()
                plugin.setup(self.con, const, self.exec_args)
                plugins.append(plugin)

        return plugins
    
    def setup(self) -> None:
        """
        Setup db connection and register resources.
        """
        # Setup connection
        self.con = duckdb.connect(database = ":memory:")
      
    def register_resources(self, resources: List[DataResource]) -> None:
        """
        Register resources.
        """

        # Write resources in db
        for res in resources:
            
            # Handle multiple paths
            if isinstance(res.path, list):
                for idx, pth in enumerate(res.tmp_pth):
                    if idx == 0:
                        sql = f"CREATE TABLE {res.name} AS SELECT * FROM '{pth}';"
                    else:
                        sql = f"COPY {res.name} FROM '{pth}' (AUTO_DETECT TRUE);"
                    self.con.execute(sql)            
            
            # Handle single path
            else:
                sql = f"CREATE TABLE {res.name} AS SELECT * FROM '{res.tmp_pth}';"
                self.con.execute(sql)

    def destroy(self) -> None:
        """
        Destory db.
        """
        self.con.close()
