"""
Dummy implementation of validation plugin.
"""
# pylint: disable=arguments-differ,too-few-public-methods
from __future__ import annotations

import typing
from typing import List

from datajudge.data.datajudge_report import DatajudgeReport
from datajudge.run.plugin.validation.validation_plugin import Validation, ValidationPluginBuilder
from datajudge.utils.commons import DUMMY
from datajudge.run.plugin.plugin_utils import exec_decorator

if typing.TYPE_CHECKING:
    from datajudge.data.data_resource import DataResource
    from datajudge.utils.config import Constraint
    from datajudge.run.plugin.base_plugin import Result


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

    @exec_decorator
    def validate(self) -> dict:
        """
        Do nothing.
        """
        return {}

    @exec_decorator
    def render_datajudge(self, result: Result) -> DatajudgeReport:
        """
        Return a DatajudgeReport.
        """
        return DatajudgeReport(self.get_lib_name(),
                               self.get_lib_version(),
                               None,
                               None,
                               None,
                               None)

    @exec_decorator
    def render_artifact(self, result: Result) -> List[tuple]:
        """
        Return a dummy report to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = dict(result.artifact)
        filename = self._fn_report.format(f"{DUMMY}.json")
        artifacts.append(self.get_render_tuple(_object, filename))
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


class ValidationBuilderDummy(ValidationPluginBuilder):
    """
    Dummy validation plugin builder.
    """
    def setup(self, *args) -> None:
        """
        Setup builder.
        """

    def build(self,
              resources: List[DataResource],
              constraints: List[Constraint]
              ) -> List[ValidationPluginDummy]:
        """
        Build a plugin.
        """
        plugins = []
        plugin = ValidationPluginDummy()
        plugin.setup(resources, constraints, self.exec_args)
        plugins.append(plugin)
        return plugins

    def filter_constraints(constraints: List[Constraint]
                           ) -> List[Constraint]:
        """
        Filter constraints by library.
        """

    def destroy(self, *args) -> None:
        """
        Destroy builder.
        """
