"""
Dummy implementation of validation plugin.
"""
# pylint: disable=unused-argument
from typing import List

from datajudge.metadata.datajudge_reports import DatajudgeReport
from datajudge.plugins.utils.plugin_utils import exec_decorator
from datajudge.plugins.validation.validation_plugin import (
    Validation, ValidationPluginBuilder)
from datajudge.utils.commons import GENERIC_DUMMY, LIBRARY_DUMMY
from datajudge.utils.config import Constraint


class ValidationPluginDummy(Validation):
    """
    Dummy implementation of validation plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.resource = None

    def setup(self,
              resource: "DataResource",
              constraint: dict,
              error_report: str,
              exec_args: dict) -> None:
        """
        Set plugin resource.
        """
        self.resource = resource
        self.constraint = constraint
        self.error_report = error_report
        self.exec_args = exec_args

    @exec_decorator
    def validate(self) -> dict:
        """
        Do nothing.
        """
        return {}

    @exec_decorator
    def render_datajudge(self, result: "Result") -> DatajudgeReport:
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
    def render_artifact(self, result: "Result") -> List[tuple]:
        """
        Return a dummy report to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = dict(result.artifact)
        filename = self._fn_report.format(f"{GENERIC_DUMMY}.json")
        artifacts.append(self.get_render_tuple(_object, filename))
        return artifacts

    @staticmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """
        return LIBRARY_DUMMY

    @staticmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """
        return LIBRARY_DUMMY


class ValidationBuilderDummy(ValidationPluginBuilder):
    """
    Dummy validation plugin builder.
    """

    def build(self,
              resources: List["DataResource"],
              constraints: List[Constraint],
              error_report: str
              ) -> List[ValidationPluginDummy]:
        """
        Build a plugin.
        """
        const = Constraint(name="",
                           title="",
                           resources=[""],
                           weight=0)
        plugins = []
        plugin = ValidationPluginDummy()
        plugin.setup(None, const, None, self.exec_args)
        plugins.append(plugin)
        return plugins

    @staticmethod
    def _filter_constraints(constraints: List[Constraint]
                            ) -> List[Constraint]:
        """
        Do nothing.
        """

    def destroy(self, *args) -> None:
        """
        Do nothing.
        """