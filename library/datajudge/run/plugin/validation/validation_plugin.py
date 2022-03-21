"""
Validation plugin abstract class module.
"""
# pylint: disable=too-few-public-methods
from abc import ABCMeta, abstractmethod
from typing import Any

from datajudge.run.plugin.base_plugin import Plugin, Result
from datajudge.utils.config import STATUS_RUNNING


class ValidationResult(Result):
    """
    Extend Result class.
    """
    def __init__(self,
                 artifact: Any = None,
                 status: str = None,
                 execution_time: float = None,
                 constraint: dict = None) -> None:
        super().__init__(artifact, status, execution_time)
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
        self.result.libraries = self.get_library()

        self.result.execution_status = STATUS_RUNNING
        self.result.artifact, \
            self.result.execution_status, \
                self.result.execution_errors, \
                    self.result.execution_time = self.validate()

        self.result.datajudge_status = STATUS_RUNNING
        self.result.datajudge_artifact, \
            self.result.datajudge_status, \
                self.result.datajudge_errors, _ = self.render_datajudge()

        self.result.datajudge_status = STATUS_RUNNING                    
        self.result.rendered_artifact, \
            self.result.rendered_status, \
                self.result.rendered_errors, _ = self.render_artifact()

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
