"""
Frictionless implementation of validation plugin.
"""
# pylint: disable=import-error,no-name-in-module,arguments-differ,no-member,too-few-public-methods
from __future__ import annotations

import typing
from copy import deepcopy
from typing import List

import frictionless
from frictionless import Report, Resource, Schema
from frictionless.exception import FrictionlessException

from datajudge.data.datajudge_report import DatajudgeReport
from datajudge.run.plugin.validation.validation_plugin import (
    Validation, ValidationPluginBuilder)
from datajudge.utils.commons import FRICTIONLESS
from datajudge.run.plugin.plugin_utils import exec_decorator

if typing.TYPE_CHECKING:
    from datajudge.data.data_resource import DataResource
    from datajudge.utils.config import Constraint, ConstraintsFrictionless
    from datajudge.run.plugin.base_plugin import Result


class ValidationPluginFrictionless(Validation):
    """
    Frictionless implementation of validation plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.resource = None
        self.constraint = None
        self.exec_args = None
        self.multiprocess = True

    def setup(self,
              resource: DataResource,
              constraint: ConstraintsFrictionless,
              exec_args: dict) -> None:
        """
        Set plugin resource.
        """
        self.resource = resource
        self.constraint = constraint
        self.exec_args = exec_args

    @exec_decorator
    def validate(self) -> Report:
        """
        Validate a Data Resource.
        """
        schema = self.rebuild_constraints()
        res = Resource(path=self.resource.tmp_pth,
                       schema=schema).validate(**self.exec_args)
        # Workaround: when using multiprocessin, we need to convert
        # the report in a dict.
        return Report(res.to_dict())

    def rebuild_constraints(self) -> Schema:
        """
        Rebuild constraints.
        """
        field_name = self.constraint.field
        field_type = self.constraint.fieldType
        val = self.constraint.value
        con_type = self.constraint.constraint
        weight = self.constraint.weight

        schema = deepcopy(self.resource.schema)

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

    @exec_decorator
    def render_datajudge(self, result: Result) -> DatajudgeReport:
        """
        Return a DatajudgeReport.
        """
        report = result.artifact
        constraint = self.constraint.dict()
        duration = report.get("time")
        valid = report.get("valid")
        spec = ["fieldName", "rowNumber", "code", "note", "description"]
        flat_report = report.flatten(spec=spec)
        errors = [dict(zip(spec, err)) for err in flat_report]

        # # If frictionless is unable to infer schema or a schema
        # # is not provided, the resource results valid, but is hard to
        # # track the thing. If no schema is detected in the resource
        # # validate, datajudge will consider the validation false
        # _schema_check = report.get("tasks")[0].resource.schema
        # if not _schema_check.get("fields", False):
        #     errors.append({
        #         "fieldName": None,
        #         "rowNumber": None,
        #         "code": None,
        #         "note": "No schema provided for resource",
        #         "description": "Check if resource as no extension"
        #     })
        #     valid = False

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
        filename = self._fn_report.format(f"{FRICTIONLESS}.json")
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
        f_constraints = self.filter_constraints(constraints)
        plugins = []
        for res in resources:
            resource = self.fetch_resource(res)
            resource.schema = self.get_schema(resource)
            for const in f_constraints:
                if resource.name in const.resources:
                    plugin = ValidationPluginFrictionless()
                    plugin.setup(resource, const, self.exec_args)
                    plugins.append(plugin)

        return plugins

    def get_schema(self,
                   resource: DataResource) -> dict:
        """
        Infer simple schema of a resource if not present.
        """
        try:
            schema = Schema(resource.schema)
            if not schema:
                schema = Schema.describe(path=resource.tmp_pth)
                if not schema:
                    return {"fields": []}
            return {"fields": [{"name": field["name"]} for field in schema["fields"]]}
        except FrictionlessException as fex:
            raise fex

    @staticmethod
    def filter_constraints(constraints: List[Constraint]
                           ) -> List[ConstraintsFrictionless]:
        return [const for const in constraints
                if const.type == FRICTIONLESS]

    def destroy(self) -> None:
        """
        Destroy builder.
        """