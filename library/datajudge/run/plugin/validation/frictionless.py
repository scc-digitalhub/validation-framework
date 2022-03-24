"""
Frictionless implementation of validation plugin.
"""
# pylint: disable=import-error,no-name-in-module,arguments-differ,no-member,too-few-public-methods
from __future__ import annotations

import typing
from copy import deepcopy
from typing import List

import frictionless
from frictionless import Report, Resource, Schema, describe_schema

from datajudge.data.datajudge_report import DatajudgeReport
from datajudge.run.plugin.base_plugin import PluginBuilder
from datajudge.run.plugin.validation.validation_plugin import (
    Validation)
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
        resource = Resource(path=self.resource.tmp_pth,
                            schema=schema)
        return frictionless.validate(resource,
                                     **self.exec_args)

    def rebuild_constraints(self) -> Schema:
        """
        Rebuild constraints.
        """
        field_name = self.constraint.field
        field_type = self.constraint.field_type
        val = self.constraint.value
        con_type = self.constraint.constraint
        severity = self.constraint.severity

        schema = deepcopy(self.resource.schema)

        for field in schema["fields"]:
            if field["name"] == field_name:
                field["error"] = {"severity": severity}
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


class ValidationBuilderFrictionless(PluginBuilder):
    """
    Validation plugin builder.
    """
    def build(self,
              resources: List[DataResource],
              constraints: List[Constraint]) -> ValidationPluginFrictionless:
        """
        Build a plugin for every resource and every constraint.
        """
        plugins = []
        for resource in resources:
            if resource.schema is None:
                resource.schema = self._infer_schema(resource.tmp_pth)

            for const in constraints:
                if resource.name in const.resources and \
                   const.type == "frictionless":
                    plugin = ValidationPluginFrictionless()
                    plugin.setup(resource, const, self.exec_args)
                    plugins.append(plugin)

        return plugins

    def _infer_schema(self, path: str) -> dict:
        """
        Infer schema of a resource.
        """
        schema = describe_schema(path=path)
        return {"fields": [{"name": field["name"]} for field in schema["fields"]]}
