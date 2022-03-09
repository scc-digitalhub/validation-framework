"""
Frictionless implementation of validation plugin.
"""
# pylint: disable=import-error,invalid-name
from __future__ import annotations
from copy import deepcopy

import typing
from typing import List

import frictionless
from frictionless import Report, Resource, Schema

from datajudge.run.plugin.base_plugin import PluginBuilder
from datajudge.run.plugin.validation.validation_plugin import Validation, ValidationResult

if typing.TYPE_CHECKING:
    from datajudge import DataResource


class ValidationPluginFrictionless(Validation):
    """
    Frictionless implementation of validation plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.resource = None
        self.constraint = None
        self.base_schema = None
        self.exec_args = None

    def setup(self,
              resource: DataResource,
              constraint: tuple,
              exec_args: dict) -> None:
        """
        Set plugin resource.
        """
        self.resource = resource
        self.constraint = constraint[0]
        self.base_schema = constraint[1]
        self.exec_args = exec_args
        self.result = ValidationResult(status=self._STATUS_INIT,
                                       constraint=self.constraint)

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

        for field in self.base_schema["fields"]:
            if field.get("name") == field_name:
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

        return Schema(self.base_schema)

    def produce_report(self,
                       obj: ValidationResult) -> tuple:
        """
        Parse the report produced by frictionless.
        """
        report = obj.artifact
        constraint = obj.constraint.dict()
        duration = report.get("time")
        valid = report.get("valid")
        spec = ["fieldName", "rowNumber", "code", "note", "description"]
        flat_report = report.flatten(spec=spec)
        errors = [dict(zip(spec, err)) for err in flat_report]
        return self.get_report_tuple(duration, constraint, valid, errors)

    def render_artifact(self, obj: Report) -> List[tuple]:
        """
        Return a rendered report ready to be persisted as artifact.
        """
        artifacts = []
        report = dict(obj)
        filename = self._fn_report.format("frictionless.json")
        artifacts.append(self.get_render_tuple(report, filename))
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
              package: list,
              exec_args: dict,
              constraints: list) -> ValidationPluginFrictionless:
        """
        Build a plugin for every resource and every constraint.
        """
        plugins = []
        for resource in package:

            res_const = []
            for const in constraints:
                if (resource.name in const.resources and
                                const.type == "frictionless"):
                    res_const.append(const)

            base_schema = {"fields": []}
            field_list = []
            for const in res_const:
                if const.field not in field_list:
                    field_list.append(const.field)
                    base_schema["fields"].append({"name": const.field})

            for const in res_const:
                plugin = ValidationPluginFrictionless()
                plugin.setup(resource, (const, deepcopy(base_schema)), exec_args)
                plugins.append(plugin)

        return plugins
