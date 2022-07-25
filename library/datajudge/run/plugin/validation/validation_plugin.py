"""
Validation plugin abstract class module.
"""

from __future__ import annotations

import typing
from abc import ABCMeta, abstractmethod
from typing import Any, List

from datajudge.run.plugin.base_plugin import Plugin, PluginBuilder
from datajudge.utils.commons import (RESULT_DATAJUDGE, RESULT_LIBRARY,
                                     RESULT_RENDERED, RESULT_WRAPPED)

if typing.TYPE_CHECKING:
    from datajudge.utils.config import Constraint


class Validation(Plugin, metaclass=ABCMeta):
    """
    Run plugin that executes validation over a Resource.
    """

    _fn_report = "report_{}"

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
