"""
Frictionless implementation of validation plugin.
"""

from __future__ import annotations

import typing
from typing import List, Union

import frictionless
from frictionless import Report, Resource, Schema
from frictionless.exception import FrictionlessException

from datajudge.data_reader.file_reader import FileReader
from datajudge.metadata import DatajudgeReport
from datajudge.run.plugin.utils.plugin_utils import exec_decorator
from datajudge.run.plugin.validation.validation_plugin import (
    Validation, ValidationPluginBuilder)
from datajudge.utils.commons import (CONSTRAINT_FRICTIONLESS_SCHEMA,
                                     LIBRARY_FRICTIONLESS)
from datajudge.utils.config import (ConstraintFrictionless,
                                    ConstraintFullFrictionless)

if typing.TYPE_CHECKING:
    from datajudge.data_reader.base_reader import DataReader
    from datajudge.metadata import DataResource
    from datajudge.run.plugin.base_plugin import Result
    from datajudge.utils.config import Constraint


class ValidationPluginFrictionless(Validation):
    """
    Frictionless implementation of validation plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.resource = None
        self.constraint = None
        self.exec_args = None
        self.exec_multiprocess = True

    def setup(self,
              data_reader: DataReader,
              resource: DataResource,
              constraint: ConstraintFrictionless,
              exec_args: dict) -> None:
        """
        Set plugin resource.
        """
        self.resource = resource
        self.constraint = constraint
        self.exec_args = exec_args
        self.data_path = data_reader.fetch_resource(self.resource.path)
        self.schema = self._rebuild_constraints()

    @exec_decorator
    def validate(self) -> Report:
        """
        Validate a Data Resource.
        """
        res = Resource(path=self.data_path,
                       schema=self.schema).validate(**self.exec_args)
        return Report(res.to_dict())

    def _rebuild_constraints(self) -> Schema:
        """
        Rebuild constraints.
        """
        if isinstance(self.constraint, ConstraintFrictionless):
            field_name = self.constraint.field
            field_type = self.constraint.fieldType
            val = self.constraint.value
            con_type = self.constraint.constraint
            weight = self.constraint.weight

            schema = self._get_schema()

            for field in schema["fields"]:
                if field["name"] == field_name:
                    field["error"] = {"weight": weight}
                    if con_type == "type":
                        field["type"] = field_type
                    elif con_type == "format":
                        field["type"] = field_type
                        field["format"] = val
                    else:
                        field["type"] = field_type
                        field["constraints"] = {con_type: val}
                    break
            return Schema(schema)

        # Otherwise return the full table schema
        return Schema(self.constraint.table_schema)

    def _get_schema(self) -> dict:
        """
        Infer simple schema of a resource if not present.
        """
        try:
            schema = Schema(self.resource.schema)
            if not schema:
                schema = Schema.describe(path=self.data_path)
                if not schema:
                    return {"fields": []}
            return {"fields": [{"name": field["name"]} for field in schema["fields"]]}
        except FrictionlessException as fex:
            raise fex

    @exec_decorator
    def render_datajudge(self, result: Result) -> DatajudgeReport:
        """
        Return a DatajudgeReport.
        """
        exec_err = result.errors
        duration = result.duration
        constraint = self.constraint.dict()

        if exec_err is None:
            report = result.artifact
            duration = report.get("time")
            valid = report.get("valid")
            spec = ["fieldName", "rowNumber", "code", "note", "description"]
            flat_report = report.flatten(spec=spec)
            errors = [dict(zip(spec, err)) for err in flat_report]
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
        filename = self._fn_report.format(f"{LIBRARY_FRICTIONLESS}.json")
        artifacts.append(self.get_render_tuple(_object, filename))
        return artifacts

    @staticmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """
        return frictionless.__name__

    @staticmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """
        return frictionless.__version__


class ValidationBuilderFrictionless(ValidationPluginBuilder):
    """
    Validation plugin builder.
    """

    def build(self,
              resources: List[DataResource],
              constraints: List[Constraint]
              ) -> List[ValidationPluginFrictionless]:
        """
        Build a plugin for every resource and every constraint.
        """
        f_constraints = self._filter_constraints(constraints)
        plugins = []
        for res in resources:
            resource = self._get_resource_deepcopy(res)
            for const in f_constraints:
                if resource.name in const.resources:
                    store = self._get_resource_store(resource)
                    data_reader = FileReader(store, self.fetch_mode, self.reader_args)
                    plugin = ValidationPluginFrictionless()
                    plugin.setup(data_reader, resource, const, self.exec_args)
                    plugins.append(plugin)

        return plugins

    @staticmethod
    def _filter_constraints(constraints: List[Constraint]
                            ) -> List[Union[ConstraintFrictionless, ConstraintFullFrictionless]]:
        """
        Filter out ConstraintFrictionless and ConstraintFullFrictionless
        """
        return [const for const in constraints
                if const.type in (LIBRARY_FRICTIONLESS, CONSTRAINT_FRICTIONLESS_SCHEMA)]

    def destroy(self) -> None:
        """
        Destroy builder.
        """
