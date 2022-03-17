"""
Dummy implementation of validation plugin.
"""
# pylint: disable=arguments-differ,too-few-public-methods
from __future__ import annotations

import typing
from typing import List

from datajudge.run.plugin.base_plugin import PluginBuilder
from datajudge.run.plugin.validation.validation_plugin import (
    Validation, ValidationResult)

if typing.TYPE_CHECKING:
    from datajudge import DataResource


class ValidationPluginDummy(Validation):
    """
    Dummy implementation of validation plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.resource = None
        self.constraints = None
        self.exec_args = None

    def setup(self,
              resource: DataResource,
              constraints: dict,
              exec_args: dict) -> None:
        """
        Set plugin resource.
        """
        self.resource = resource
        self.constraints = constraints
        self.exec_args = exec_args

    def validate(self) -> dict:
        """
        Do nothing.
        """
        return {}

    def rebuild_constraints(self) -> dict:
        """
        Do nothing.
        """
        return {}

    def produce_report(self,
                       obj: ValidationResult) -> tuple:
        """
        Do nothing.
        """
        return self.get_report_tuple(None, None, None, None)

    def render_artifact(self, obj: dict) -> List[tuple]:
        """
        Return a dummy report to be persisted as artifact.
        """
        artifacts = []
        report = obj
        filename = self._fn_report.format("dummy.json")
        artifacts.append(self.get_render_tuple(report, filename))
        return artifacts

    @staticmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """
        return None

    @staticmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """
        return None


class ValidationBuilderDummy(PluginBuilder):
    """
    Validation plugin builder.
    """
    def build(self,
              package: list,
              exec_args: dict,
              constraints: list) -> ValidationPluginDummy:
        """
        Build a plugin.
        """
        plugins = []
        for resource in package:
            plugin = ValidationPluginDummy()
            plugin.setup(resource, constraints, exec_args)
            plugins.append(plugin)
        return plugins
