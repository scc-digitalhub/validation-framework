"""
Dummy implementation of validation plugin.
"""
# pylint: disable=import-error,invalid-name
from typing import Any, List, Optional

from datajudge.run.validation.validation_plugin import (RenderTuple,
                                                        ReportTuple,
                                                        Validation)


FN_REPORT = "report_dummy.json"


class ValidationPluginDummy(Validation):
    """
    Dummy implementation of validation plugin.
    """

    def update_library_info(self) -> None:
        """
        Update run's info about the validation framework used.
        """
        self.lib_name = None
        self.lib_version = None

    def parse_report(self,
                     report: Any,
                     schema_path: Optional[str] = None
                     ) -> ReportTuple:
        """
        Return none.
        """
        return ReportTuple(None, None, None)

    def validate_report(self, report: Any) -> None:
        """
        Do nothing.
        """

    def validate(self,
                 res_name: str,
                 data_path: str,
                 constraints: Optional[dict] = None,
                 schema_path: Optional[str] = None,
                 kwargs: Optional[dict] = None) -> dict:
        """
        Return fake empty report.
        """
        report = self.registry.get_result(res_name)
        if report is not None:
            return report
        
        report = {}

        self.registry.add_result(res_name, report, None)

        return report

    def render_object(self,
                      obj: Any) -> List[RenderTuple]:
        """
        Return a dummy report to be persisted as artifact.
        """
        return [RenderTuple({}, FN_REPORT)]
