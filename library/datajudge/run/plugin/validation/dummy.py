"""
Dummy implementation of validation plugin.
"""
# pylint: disable=import-error,invalid-name
from typing import Any, List

from datajudge.run.plugin.validation.validation_plugin import Validation


class ValidationPluginDummy(Validation):
    """
    Dummy implementation of validation plugin.
    """

    def update_library_info(self) -> None:
        """
        Do nothing.
        """

    def rebuild_constraint(self, constraints: Any) -> None:
        """
        Do nothing.
        """

    def parse_report(self, report: Any) -> tuple:
        """
        Return none.
        """
        return self.get_report_tuple(None, None, None)

    def validate_report(self, report: Any) -> None:
        """
        Do nothing.
        """

    def validate(self,
                 res_name: str,
                 data_path: str,
                 exec_args: dict) -> dict:
        """
        Generate dummy report.
        """
        return {}

    def get_outcome(self, obj: Any) -> str:
        """
        Return status of the execution.
        """
        return self._VALID_STATUS

    def render_artifact(self, obj: Any) -> List[tuple]:
        """
        Return a dummy report to be persisted as artifact.
        """
        report = {}
        filename = self._fn_report.format("dummy.json")
        return [self.get_render_tuple(report, filename)]
