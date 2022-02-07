"""
Validation plugin abstract class module.
"""
# pylint: disable=import-error,invalid-name
from __future__ import annotations
from collections import namedtuple

from abc import ABCMeta, abstractmethod
from typing import Any, List, Optional

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
                 data_path: str,
                 schema_path: str,
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
