"""
Validation plugin abstract class module.
"""
# pylint: disable=import-error,invalid-name
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from typing import Any, Optional

from datajudge.data.datajudge_report import DatajudgeReport
from datajudge.run.plugin.base_plugin import Plugin


ReportTuple = namedtuple("ReportTuple", ("time", "valid", "errors"))


class Validation(Plugin, metaclass=ABCMeta):
    """
    Run plugin that executes validation over a Resource.
    """

    _fn_report = "report_{}"

    @abstractmethod
    def rebuild_constraint(self) -> Any:
        """
        Rebuild input constraints.
        """

    @abstractmethod
    def parse_report(self,
                     report: Any,
                     schema_path: Optional[str] = None
                     ) -> ReportTuple:
        """
        Parse the report produced by the validation framework.
        """

    @abstractmethod
    def validate_report(self,
                        report: Optional[Any] = None
                        ) -> None:
        """
        Check a report before log/persist it.
        """

    @abstractmethod
    def validate(self,
                 res_name: str,
                 data_path: str,
                 exec_args: dict) -> Any:
        """
        Validate a resource.
        """

    def execute(self, *args, **kwargs) -> Any:
        """
        Execute plugin main operation.
        """
        return self.validate(*args, **kwargs)

    def render_datajudge(self,
                         report: Any,
                         res_name: str) -> DatajudgeReport:
        """
        Return a DatajudgeReport.
        """
        parsed = self.parse_report(report)
        return DatajudgeReport(self.lib_name,
                               self.lib_version,
                               parsed.time,
                               parsed.valid,
                               parsed.errors)

    @staticmethod
    def get_report_tuple(time: float,
                         valid: bool,
                         errors: list) -> ReportTuple:
        """
        Return ReportTuple.
        """
        return ReportTuple(time, valid, errors)
