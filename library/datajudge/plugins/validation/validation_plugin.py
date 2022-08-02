"""
Validation plugin abstract class module.
"""

from __future__ import annotations

import typing
from abc import ABCMeta, abstractmethod
from typing import Any, List

from datajudge.plugins.base_plugin import Plugin, PluginBuilder
from datajudge.utils.commons import (RESULT_DATAJUDGE, RESULT_LIBRARY,
                                     RESULT_RENDERED, RESULT_WRAPPED)

if typing.TYPE_CHECKING:
    from datajudge.utils.config import Constraint


class Validation(Plugin, metaclass=ABCMeta):
    """
    Run plugin that executes validation over a Resource.
    """

    _fn_report = "report_{}"

    def __init__(self) -> None:
        super().__init__()
        self.constraint = None
        self.error_report = None

    def execute(self) -> dict:
        """
        Method that call specific execution.
        """
        self.logger.info(
            f"Execute validation: plugin {self.lib_name} {self._id}, constraint {self.constraint.name}, resources {self.constraint.resources}")
        lib_result = self.validate()
        self.logger.info(
            f"Render datajudge result: plugin {self.lib_name} {self._id}")
        dj_result = self.render_datajudge(lib_result)
        self.logger.info(f"Render artifact: plugin {self.lib_name} {self._id}")
        render_result = self.render_artifact(lib_result)
        return {
            RESULT_WRAPPED: lib_result,
            RESULT_DATAJUDGE: dj_result,
            RESULT_RENDERED: render_result,
            RESULT_LIBRARY: self.get_library()
        }

    @abstractmethod
    def validate(self) -> Any:
        """
        Validate a resource.
        """

    @staticmethod
    def _render_error_type(code: str) -> dict:
        """
        Return standard errors record format.
        """
        return {"type": code}

    def _parse_error_report(self,
                            error_list: list) -> list:
        """
        Return a list of record according to user parameter.
        """
        if self.error_report == "count":
            return []
        if self.error_report == "partial":
            if len(error_list) <= 100:
                return error_list
            return error_list[:100]
        if self.error_report == "full":
            return error_list

    @staticmethod
    def _get_errors(count: int = 0,
                    records: list = None) -> dict:
        """
        Return a common error structure.
        """
        if records is None:
            records = []
        return {
            "count": count,
            "records": records
        }


class ValidationPluginBuilder(PluginBuilder):
    """
    Validation plugin builder.
    """

    @staticmethod
    @abstractmethod
    def _filter_constraints(constraints: List[Constraint]
                            ) -> List[Constraint]:
        """
        Filter constraints by library.
        """
