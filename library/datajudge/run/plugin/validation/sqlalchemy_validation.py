"""
SQLAlchemy implementation of validation plugin.
"""

from __future__ import annotations

import typing
from copy import deepcopy
from typing import List

import sqlalchemy

from datajudge.data_reader.pandas_dataframe_reader import PandasDataFrameReader
from datajudge.metadata.datajudge_reports import DatajudgeReport
from datajudge.run.plugin.utils.plugin_utils import exec_decorator
from datajudge.run.plugin.utils.sql_checks import evaluate_validity
from datajudge.run.plugin.validation.validation_plugin import (
    Validation, ValidationPluginBuilder)
from datajudge.store_artifact.sql_artifact_store import SQLArtifactStore
from datajudge.utils.commons import DATAREADER_NATIVE, LIBRARY_SQLALCHEMY
from datajudge.utils.exceptions import ValidationError
from datajudge.utils.utils import flatten_list, listify

if typing.TYPE_CHECKING:
    from datajudge.metadata.data_resource import DataResource
    from datajudge.run.plugin.base_plugin import Result
    from datajudge.utils.config import Constraint, ConstraintSqlAlchemy


class ValidationPluginSqlAlchemy(Validation):
    """
    SQLAlchemy implementation of validation plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.df = None
        self.exec_multiprocess = True

    def setup(self,
              data_reader: str,
              constraint: ConstraintSqlAlchemy,
              exec_args: dict) -> None:
        """
        Set plugin resource.
        """
        self.constraint = constraint
        self.exec_args = exec_args
        self.df = data_reader.fetch_resource("sql://resource",
                                             query=constraint.query)

    @exec_decorator
    def validate(self) -> dict:
        """
        Validate a Data Resource.
        """
        try:
            valid, errors = evaluate_validity(self.df,
                                              self.constraint.check,
                                              self.constraint.expect,
                                              self.constraint.value)
            return {
                "result": self.df.to_dict(),
                "valid": valid,
                "errors": listify(errors)
            }
        except Exception as ex:
            raise ex

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
            self.logger.error(
                f"Execution error {str(exec_err)} for plugin {self._id}")
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
        filename = self._fn_report.format(f"{LIBRARY_SQLALCHEMY}.json")
        artifacts.append(self.get_render_tuple(_object, filename))
        return artifacts

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
        self._setup()

        f_constraint = self._filter_constraints(constraints)
        f_resources = self._filter_resources(resources, f_constraint)
        grouped_constraints = self._regroup_constraint_resources(
            f_constraint, f_resources)

        plugins = []
        for pack in grouped_constraints:
            store = pack["store"]
            constraint = pack["constraint"]
            data_reader = PandasDataFrameReader(store, self.fetch_mode, self.reader_args)
            plugin = ValidationPluginSqlAlchemy()
            plugin.setup(data_reader, constraint, self.exec_args)
            plugins.append(plugin)

        return plugins

    def _setup(self) -> None:
        """
        Filter builder store to keep only SQLStores and set `native` mode for
        reading data to return a connection string to a db.
        """
        #
        self.fetch_mode = DATAREADER_NATIVE
        self.stores = [store for store in self.stores if isinstance(
            store, SQLArtifactStore)]
        if not self.stores:
            raise ValidationError(
                "There must be at least a SQLStore to use sqlalchemy validator.")

    @staticmethod
    def _filter_constraints(constraints: List[Constraint]
                            ) -> List[ConstraintSqlAlchemy]:
        """
        Filter out ConstraintSqlAlchemy.
        """
        return [const for const in constraints if const.type == LIBRARY_SQLALCHEMY]

    def _filter_resources(self,
                          resources: List[DataResource],
                          constraints: List[Constraint]
                          ) -> List[DataResource]:
        """
        Filter resources used by validator.
        """
        res_names = set(flatten_list(
            [deepcopy(const.resources) for const in constraints]))
        res_to_validate = [res for res in resources if res.name in res_names]
        st_names = [store.name for store in self.stores]
        res_in_db = [res for res in res_to_validate if res.store in st_names]
        return res_in_db

    @staticmethod
    def _regroup_constraint_resources(constraints: List[Constraint],
                                      resources: List[DataResource]
                                      ) -> list:
        """
        Check univocity of resources location and return connection
        string for db access.
        """
        constraint_connection = []

        for const in constraints:
            res_stores = [res.store for res in resources]

            store_num = len(set(res_stores))
            if store_num > 1:
                raise ValidationError(
                    f"Resources for constraint `{const.name}` are not in the same database.")
            if store_num == 0:
                raise ValidationError(
                    f"No resources for constraint `{const.name}` are in a configured store.")

            constraint_connection.append({
                "constraint": const,
                "store": res_stores[0]
            })

        return constraint_connection

    def destroy(self) -> None:
        """
        Destory plugins.
        """
