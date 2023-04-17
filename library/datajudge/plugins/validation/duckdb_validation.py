"""
DuckDB implementation of validation plugin.
"""
# pylint: disable=import-error
import shutil
from copy import deepcopy
from pathlib import Path
from typing import List, Any

import duckdb
from duckdb import CatalogException

from datajudge.metadata.datajudge_reports import DatajudgeReport
from datajudge.plugins.utils.plugin_utils import exec_decorator
from datajudge.plugins.utils.sql_checks import evaluate_validity
from datajudge.plugins.validation.validation_plugin import (
    Validation,
    ValidationPluginBuilder,
)
from datajudge.utils.commons import (
    POLARS_DATAFRAME_DUCKDB_READER,
    PANDAS_DATAFRAME_DUCKDB_READER,
    DEFAULT_DIRECTORY,
    LIBRARY_DUCKDB,
    CONSTRAINT_SQL_CHECK_ROWS,
    CONSTRAINT_SQL_CHECK_VALUE,
)
from datajudge.utils.utils import flatten_list, get_uiid, listify


class ValidationPluginDuckDB(Validation):
    """
    DuckDB implementation of validation plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.db = None
        self.exec_multiprocess = True

    def setup(
        self,
        data_reader: "NativeReader",
        db: str,
        constraint: "ConstraintDuckDB",
        error_report: str,
        exec_args: dict,
    ) -> None:
        """
        Set plugin resource.
        """
        self.data_reader = data_reader
        self.db = db
        self.constraint = constraint
        self.error_report = error_report
        self.exec_args = exec_args

    @exec_decorator
    def validate(self) -> dict:
        """
        Validate a Data Resource.
        """
        try:
            data = self.data_reader.fetch_data(self.db, self.constraint.query)
            value = self._filter_result(data)
            valid, errors = evaluate_validity(
                value, self.constraint.expect, self.constraint.value
            )
            result = self._shorten_data(data)
            return {"result": result, "valid": valid, "error": errors}
        except Exception as ex:
            raise ex

    def _filter_result(self, data: Any) -> Any:
        """
        Return value or size of DataFrame for SQL checks.
        """
        if self.constraint.check == CONSTRAINT_SQL_CHECK_VALUE:
            return self.data_reader.return_first_value(data)
        elif self.constraint.check == CONSTRAINT_SQL_CHECK_ROWS:
            return self.data_reader.return_length(data)

    def _shorten_data(self, data: Any) -> Any:
        """
        Return a short version of data.
        """
        return self.data_reader.return_head(data)

    @exec_decorator
    def render_datajudge(self, result: "Result") -> DatajudgeReport:
        """
        Return a DatajudgeReport.
        """
        exec_err = result.errors
        duration = result.duration
        constraint = self.constraint.dict()
        errors = self._get_errors()

        if exec_err is None:
            valid = result.artifact.get("valid")

            if not valid:
                total_count = 1
                errors_list = [self._render_error_type("sql-check-error")]
                parsed_error_list = self._parse_error_report(errors_list)
                errors = self._get_errors(total_count, parsed_error_list)

        else:
            self.logger.error(f"Execution error {str(exec_err)} for plugin {self._id}")
            valid = False

        return DatajudgeReport(
            self.get_lib_name(),
            self.get_lib_version(),
            duration,
            constraint,
            valid,
            errors,
        )

    @exec_decorator
    def render_artifact(self, result: "Result") -> List[tuple]:
        """
        Return a rendered report ready to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = dict(result.artifact)
        filename = self._fn_report.format(f"{LIBRARY_DUCKDB}.json")
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


class ValidationBuilderDuckDB(ValidationPluginBuilder):
    """
    DuckDB validation plugin builder.
    """

    def build(
        self,
        resources: List["DataResource"],
        constraints: List["Constraint"],
        error_report: str,
    ) -> List[ValidationPluginDuckDB]:
        """
        Build a plugin for every resource and every constraint.
        """
        self._setup_connection()
        f_constraint = self._filter_constraints(constraints)
        f_resources = self._filter_resources(resources, f_constraint)
        self._register_resources(f_resources)
        self._tear_down_connection()

        plugins = []
        for const in f_constraint:
            data_reader = self._get_data_reader(PANDAS_DATAFRAME_DUCKDB_READER, store)
            plugin = ValidationPluginDuckDB()
            plugin.setup(
                data_reader, self.tmp_db.as_posix(), const, error_report, self.exec_args
            )
            plugins.append(plugin)

        return plugins

    def _setup_connection(self) -> None:
        """
        Setup db connection.
        """
        self.tmp_db = Path(DEFAULT_DIRECTORY, get_uiid(), "tmp.duckdb")
        self.tmp_db.parent.mkdir(parents=True, exist_ok=True)
        self.con = duckdb.connect(database=self.tmp_db.as_posix(), read_only=False)

    @staticmethod
    def _filter_resources(
        resources: List["DataResource"], constraints: List["Constraint"]
    ) -> List["DataResource"]:
        """
        Filter resources used by validator.
        """
        res_names = set(
            flatten_list([deepcopy(const.resources) for const in constraints])
        )
        return [res for res in resources if res.name in res_names]

    def _register_resources(self, resources: List["DataResource"]) -> None:
        """
        Register resources in db.
        """
        for resource in resources:
            store = self._get_resource_store(resource)

            # If resource is already registered, continue
            try:
                if bool(self.con.table(f"{resource.name}")):
                    continue
            except CatalogException:
                pass

            # Handle multiple paths: crate a table for
            # first file, then append. Load data from Polars DF
            for idx, pth in enumerate(listify(resource.path)):
                build_reader
                data_reader = self._get_data_reader(
                    POLARS_DATAFRAME_DUCKDB_READER, store
                )
                df = data_reader.fetch_data(pth)
                if idx == 0:
                    sql = f"CREATE TABLE {resource.name} AS SELECT * FROM df;"
                else:
                    sql = f"INSERT INTO {resource.name} SELECT * FROM df;"
                self.con.execute(sql)

    def _tear_down_connection(self) -> None:
        """
        Close connection.
        """
        self.con.close()

    @staticmethod
    def _filter_constraints(
        constraints: List["Constraint"],
    ) -> List["ConstraintDuckDB"]:
        """
        Filter out "ConstraintDuckDB".
        """
        return [const for const in constraints if const.type == LIBRARY_DUCKDB]

    def destroy(self) -> None:
        """
        Destory db.
        """
        shutil.rmtree(self.tmp_db.parent, ignore_errors=True)
