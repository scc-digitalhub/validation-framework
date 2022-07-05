"""
SQLAlchemy implementation of validation plugin.
"""
# pylint: disable=import-error,no-name-in-module,arguments-differ,no-member,too-few-public-methods
from __future__ import annotations

import typing
from copy import deepcopy
from typing import List

import pandas as pd
from sqlalchemy import create_engine
import sqlalchemy

from datajudge.data import DatajudgeReport
from datajudge.run.plugin.plugin_utils import exec_decorator
from datajudge.run.plugin.validation.validation_plugin import Validation, ValidationPluginBuilder
from datajudge.store_artifact.sql_artifact_store import SQLArtifactStore
from datajudge.utils.commons import SQLALCHEMY
from datajudge.utils.exceptions import ValidationError
from datajudge.run.plugin.utils.sql_checks import evaluate_validity
from datajudge.utils.utils import flatten_list, listify

if typing.TYPE_CHECKING:
    from datajudge.data import DataResource
    from datajudge.run.plugin.base_plugin import Result
    from datajudge.utils.config import Constraint, ConstraintsSqlAlchemy


class ValidationPluginSqlAlchemy(Validation):
    """
    SQLAlchemy implementation of validation plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.conn_str = None
        self.constraint = None
        self.exec_args = None
        self.exec_multiprocess = True

    def setup(self,
              conn_str: str,
              constraint: str,
              exec_args: dict) -> None:
        """
        Set plugin resource.
        """
        self.conn_str = conn_str
        self.constraint = constraint
        self.exec_args = exec_args
        self.parse_args()

    @exec_decorator
    def validate(self) -> dict:
        """
        Validate a Data Resource.
        """
        try:
            engine = create_engine(self.conn_str)
            result = pd.read_sql(self.constraint.query, engine)
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
            engine.dispose()

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
        filename = self._fn_report.format(f"{SQLALCHEMY}.json")
        artifacts.append(self.get_render_tuple(_object, filename))
        return artifacts

    def parse_args(self):
        pass

    @staticmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """
        return sqlalchemy.__name__

    @staticmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """
        return sqlalchemy.__version__


class ValidationBuilderSqlAlchemy(ValidationPluginBuilder):
    """
    SqlAlchemy validation plugin builder.
    """
    def build(self,
              resources: List[DataResource],
              constraints: List[Constraint]
              ) -> List[ValidationPluginSqlAlchemy]:
        """
        Build a plugin for every resource and every constraint.
        """
        self.setup()
        self.check_args()

        f_constraint = self.filter_constraints(constraints)
        f_resources = self.filter_resources(resources, f_constraint)
        grouped_constraints = self.regroup_constraint_resources(f_constraint, f_resources)

        plugins = []
        for const in grouped_constraints:
            plugin = ValidationPluginSqlAlchemy()
            plugin.setup(const["conn_string"], const["constraint"], self.exec_args)
            plugins.append(plugin)

        return plugins

    def setup(self) -> None:
        """
        Filter builder store to keep only SQLStores and set file format.
        """
        self.file_format = "sql"
        self.stores = [store for store in self.stores if isinstance(store, SQLArtifactStore)]
        if not self.stores:
            raise ValidationError("There must be at least a SQLStore to use sqlalchemy validator.")

    def check_args(self) -> None:
        pass

    @staticmethod
    def filter_constraints(constraints: List[Constraint]
                           ) -> List[ConstraintsSqlAlchemy]:
        return [const for const in constraints if const.type==SQLALCHEMY]

    def filter_resources(self,
                         resources: List[DataResource],
                         constraints: List[Constraint]
                         ) -> List[DataResource]:
        """
        Filter resources used by validator.
        """
        res_names = set(flatten_list([deepcopy(const.resources) for const in constraints]))
        res_to_validate = [res for res in resources if res.name in res_names]
        st_names = [store.name for store in self.stores]
        res_in_db = [res for res in res_to_validate if res.store in st_names]
        return res_in_db            

    def regroup_constraint_resources(self,
                                     constraints: List[Constraint],
                                     resources: List[DataResource]
                                     ) -> list:
        """
        Check univocity of resources location and return connection
        string for db access.
        """
        constraint_connection = []

        for const in constraints:
            
            conn_strings = []
            for res in resources:
                if res.name in const.resources:
                    resource = self.fetch_resource(res)
                    conn_strings.append(resource.tmp_pth)
            if len(set(conn_strings)) > 1:
                raise ValidationError("Resources must be in the same database.")
        
            try:
                constraint_connection.append({
                    "constraint": const,
                    "conn_string": conn_strings[0]
                })
            except IndexError:
                raise ValidationError("At least one resource must be in a database.")

        return constraint_connection

    def destroy(self) -> None:
        """
        Destory plugins.
        """
