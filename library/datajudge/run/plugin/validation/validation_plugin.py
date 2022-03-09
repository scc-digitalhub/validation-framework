"""
Validation plugin abstract class module.
"""
# pylint: disable=import-error,invalid-name
import time
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from typing import Any

from datajudge.data.datajudge_report import DatajudgeReport
from datajudge.run.plugin.base_plugin import Plugin, Result


ReportTuple = namedtuple("ReportTuple", ("time", "constraint", "valid", "errors"))


class ValidationResult(Result):
    """
    Extend Result class.
    """
    def __init__(self,
                 artifact: Any = None,
                 status: str = None,
                 time: float = None,
                 constraint: dict = None) -> None:
        super().__init__(artifact, status, time)
        self.constraint = constraint


class Validation(Plugin, metaclass=ABCMeta):
    """
    Run plugin that executes validation over a Resource.
    """

    _fn_report = "report_{}"

    def execute(self) -> Result:
        """
        Method that call specific execution.
        """
        try:
            self.result.status = self._STATUS_RUNNING
            start = time.perf_counter()
            self.result.artifact = self.validate()
            self.result.time = round(time.perf_counter() - start, 2)
            self.result.status = self._STATUS_FINISHED
        except Exception:
            self.result.status = self._STATUS_ERROR

        return self.result

    @abstractmethod
    def validate(self) -> Any:
        """
        Validate a resource.
        """

    @abstractmethod
    def rebuild_constraints(self) -> Any:
        """
        Rebuild input constraints.
        """

    @abstractmethod
    def produce_report(self,
                       obj: ValidationResult) -> ReportTuple:
        """
        Produce datajudge report by parsing framework
        results.
        """

    def render_datajudge(self,
                         obj: ValidationResult) -> DatajudgeReport:
        """
        Return a DatajudgeReport.
        """
        parsed = self.produce_report(obj)
        return DatajudgeReport(self.get_lib_name(),
                               self.get_lib_version(),
                               parsed.time,
                               parsed.constraint,
                               parsed.valid,
                               parsed.errors)

    @staticmethod
    def get_report_tuple(time: float,
                         constraint: dict,
                         valid: bool,
                         errors: list) -> ReportTuple:
        """
        Return ReportTuple.
        """
        return ReportTuple(time, constraint, valid, errors)
