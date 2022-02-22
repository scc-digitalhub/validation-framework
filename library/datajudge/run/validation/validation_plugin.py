"""
Validation plugin abstract class module.
"""
# pylint: disable=import-error,invalid-name
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from typing import Any, List, Optional

from datajudge.run.results_registry import ResultsRegistry


ReportTuple = namedtuple("ReportTuple",
                         ("time", "valid", "errors"))
RenderTuple = namedtuple("RenderTuple",
                         ("object", "filename"))


class Validation(metaclass=ABCMeta):
    """
    Run plugin that executes validation over a Resource.
    """

    def __init__(self) -> None:
        self.lib_name = None
        self.lib_version = None
        self.registry = ResultsRegistry()
        self.update_library_info()

    @abstractmethod
    def update_library_info(self) -> None:
        """
        Update run's info about the validation framework used.
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
                 constraints: Optional[dict] = None,
                 schema_path: Optional[str] = None,
                 kwargs: Optional[dict] = None) -> Any:
        """
        Validate a resource.
        """

    @abstractmethod
    def render_object(self,
                      obj: Any) -> List[RenderTuple]:
        """
        Return a rendered report ready to be persisted as artifact.
        """

    # Getters

    def get_lib_name(self) -> str:
        return self.lib_name
    
    def get_lib_version(self) -> str:
        return self.lib_version
    
    def get_lib(self) -> dict:
        return {
                "libName": self.lib_name,
                "libVersion": self.lib_version
        }
