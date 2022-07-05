"""
DuckDB implementation of validation plugin.
"""
# pylint: disable=import-error,no-name-in-module,arguments-differ,no-member,too-few-public-methods
from __future__ import annotations

import shutil
import typing
from copy import deepcopy
from pathlib import Path
from typing import List

import duckdb

from datajudge.data import DatajudgeReport
from datajudge.run.plugin.plugin_utils import exec_decorator
from datajudge.run.plugin.validation.validation_plugin import Validation, ValidationPluginBuilder
from datajudge.utils.commons import DUCKDB
from datajudge.run.plugin.utils.sql_checks import evaluate_validity
from datajudge.utils.utils import flatten_list, listify

if typing.TYPE_CHECKING:
    from datajudge.data import DataResource
    from datajudge.run.plugin.base_plugin import Result
    from datajudge.utils.config import Constraint, ConstraintsDuckDB


class ValidationPluginDuckDB(Validation):
    """
    DuckDB implementation of validation plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.db = None
        self.constraint = None
        self.exec_args = None
        self.exec_multiprocess = True

    def setup(self,
              db: str,
              constraint: str,
              exec_args: dict) -> None:
        """
        Set plugin resource.
        """
        self.db = db
        self.constraint = constraint
        self.exec_args = exec_args
        self.parse_args()

    @exec_decorator
    def validate(self) -> dict:
        """
        Validate a Data Resource.
        """
        try:
            conn = duckdb.connect(database=self.db, read_only=True)
            conn.execute(self.constraint.query)
            result = conn.fetchdf()    
            valid, errors = evaluate_validity(result,
                                              self.constraint.check,
                                              self.constraint.expect,
                                              self.constraint.value)
            return {
                "result": result.to_dict(),
                "valid": valid,
                "errors": listify(errors)
            }
        except Exception as ex:
            raise ex
        finally:
            conn.close()

    @exec_decorator
    def render_datajudge(self, result: Result) -> DatajudgeReport:
        """
        Return a DatajudgeReport.
        """
        exec_err = result.errors
        duration = result.duration
        constraint = self.constraint.dict()

        if exec_err is None:
            valid = result.artifact.get("valid")
            errors = result.artifact.get("errors")
        else:
            self.logger.error(f"Execution error {str(exec_err)} for plugin {self._id}")
            valid = False
            errors = None

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

    def parse_args(self):
        pass

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


class ValidationBuilderDuckDB(ValidationPluginBuilder):
    """
    DuckDB validation plugin builder.
    """
    def build(self,
              resources: List[DataResource],
              constraints: List[Constraint]
              ) -> List[ValidationPluginDuckDB]:
        """
        Build a plugin for every resource and every constraint.
        """
        self.check_args()

        self.setup_connection()
        f_constraint = self.filter_constraints(constraints)
        f_resources = self.filter_resources(resources, f_constraint)
        self.register_resources(f_resources)
        self.tear_down_connection()

        plugins = []
        for const in f_constraint:
            plugin = ValidationPluginDuckDB()
            plugin.setup(self.tmp_db, const, self.exec_args)
            plugins.append(plugin)

        return plugins

    def check_args(self) -> None:
        pass

    def setup_connection(self) -> None:
        """
        Setup db connection.
        """
        self.tmp_db = "./tmp/tmp.duckdb"
        Path(self.tmp_db).parent.mkdir(parents=True, exist_ok=True)
        self.con = duckdb.connect(database=self.tmp_db, read_only=False)

    def filter_resources(self,
                         resources: List[DataResource],
                         constraints: List[Constraint]
                         ) -> List[DataResource]:
        """
        Filter resources used by validator.
        """
        res_names = set(flatten_list([deepcopy(const.resources) for const in constraints]))
        return [res for res in resources if res.name in res_names]

    def register_resources(self,
                           resources: List[DataResource]
                           ) -> None:
        """
        Register resources in db.
        """
        for res in resources:
            resource = self.fetch_resource(res)

            # If resource is already registered, continue
            try:
                if bool(self.con.table(f"{resource.name}")):
                    continue
            except RuntimeError:
                pass

            # Handle multiple paths
            if isinstance(resource.path, list):
                for idx, pth in enumerate(resource.tmp_pth):
                    if idx == 0:
                        sql = f"CREATE TABLE {resource.name} AS SELECT * FROM '{pth}';"
                    else:
                        sql = f"COPY {resource.name} FROM '{pth}' (AUTO_DETECT TRUE);"
                    self.con.execute(sql)

            # Handle single path
            else:
                sql = f"CREATE TABLE {resource.name} AS SELECT * FROM '{resource.tmp_pth}';"
                self.con.execute(sql)

    def tear_down_connection(self) -> None:
        """
        Close connection.
        """
        self.con.close()

    @staticmethod
    def filter_constraints(constraints: List[Constraint]
                           ) -> List[ConstraintsDuckDB]:
        return [const for const in constraints if const.type == DUCKDB]

    def destroy(self) -> None:
        """
        Destory db.
        """
        shutil.rmtree(Path(self.tmp_db).parent)
