"""
Frictionless implementation of validation plugin.
"""
# pylint: disable=import-error,no-name-in-module,arguments-differ,no-member,too-few-public-methods
from __future__ import annotations

import re
import typing
from copy import deepcopy
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
        valid, errors = self.evaluate_validity(result,
                                               self.constraint.expect,
                                               self.constraint.value)
        return {
            "result": result.to_dict(),
            "valid": valid,
            "errors": errors
        }

    def evaluate_validity(self,
                            result: pd.DataFrame,
                            expect: str,
                            value: Any) -> Tuple[bool, list]:
        """
        Evaluate validity of query results.
        """
        if expect == EMPTY:
            return self.evaluate_empty(result, empty=True)
        elif expect == NON_EMPTY:
            return self.evaluate_empty(result, empty=False)
        elif expect == EXACT:
            return self.evaluate_exact(result, value)
        elif expect == RANGE:
            return self.evaluate_range(result, value)
        else:
            raise NotImplementedError

    @staticmethod
    def evaluate_empty(result: pd.DataFrame,
                       empty: bool) -> tuple:
        """
        Evaluate table emptiness.
        """
        try:
            if empty:
                if result.empty:
                    return True, None
                return False, "Table is not empty."
            else:
                if not result.empty:
                    return True, None
                return False, "Table is empty."
        except Exception as ex:
            return False, ex.args

    @staticmethod
    def evaluate_exact(result: pd.DataFrame,
                       value: Any) -> tuple:
        """
        Evaluate if a value is exactly as expected.
        """
        try:
            res_val = result.iloc[0, 0]
            if bool(res_val == value):
                return True, None
            return False, f"Expected value {value}, instead got {res_val}."
        except Exception as ex:
            return False, ex.args

    @staticmethod
    def evaluate_range(result: pd.DataFrame,
                       _range: Any) -> tuple:
        try:
            res_val = result.iloc[0, 0]
            
            regex = r"^(\[|\()([+-]?[0-9]+[.]?[0-9]*),\s?([+-]?[0-9]+[.]?[0-9]*)(\]|\))$"
            mtc = re.match(regex, _range)
            if mtc:
                # Upper and lower limit type
                ll = mtc.group(1)
                ul = mtc.group(4)
                
                # Values
                _min = float(mtc.group(2))
                _max = float(mtc.group(3))
                
                # Value to check
                cv = float(res_val)

                if ll == "[" and ul == "]":
                    valid = (_min <= cv <= _max)
                elif ll == "[" and ul == ")":
                    valid = (_min <= cv < _max)
                elif ll == "(" and ul == "]":
                    valid = (_min < cv <= _max)
                elif ll == "(" and ul == ")":
                    valid = (_min < cv < _max)

                if valid:
                    return True, None
                return False, f"Expected value between {ll}{mtc.group(2)}, \
                                {mtc.group(3)}{ul}."
            return False, "Invalid range format."

        except Exception as ex:
            return False, ex.args

    @exec_decorator
    def render_datajudge(self, result: Result) -> DatajudgeReport:
        """
        Return a DatajudgeReport.
        """
        constraint = self.constraint.dict()
        duration = result.duration
        valid = result.artifact.get("valid")
        errors = result.artifact.get("errors")
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
            _object = {"errors": result.errors}
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
    
    def __init__(self, exec_args: dict) -> None:
        super().__init__(exec_args),
        self.setup()
    
    def setup(self) -> None:
        """
        Setup db connection and register resources.
        """
        # Setup connection
        self.con = duckdb.connect(database = ":memory:")
    
    def build(self,
              resources: List[DataResource],
              constraints: List[Constraint]) -> ValidationPluginDuckDB:
        """
        Build a plugin for every resource and every constraint.
        """
        # Filter resource used
        res_names = set(flatten_list(
                            [deepcopy(const.resources) for const in constraints if 
                                const.type == "duckdb"]))
        res_to_register = [res for res in resources if res.name in res_names]
        self.register_resources(res_to_register)

        import pdb; pdb.set_trace()

        plugins = []
        for const in constraints:
            if const.type == "duckdb":
                plugin = ValidationPluginDuckDB()
                plugin.setup(self.con, const, self.exec_args)
                plugins.append(plugin)

        return plugins
      
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
