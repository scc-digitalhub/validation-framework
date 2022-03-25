"""
Validation plugin abstract class module.
"""
# pylint: disable=too-few-public-methods
from __future__ import annotations

import typing
from abc import ABCMeta, abstractmethod
from typing import Any, List

from datajudge.run.plugin.base_plugin import Plugin, PluginBuilder
from datajudge.utils.commons import (RES_WRAP, RES_DJ,
                                     RES_RENDER, RES_LIB)

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
        lib_result = self.validate()
        dj_result = self.render_datajudge(lib_result)
        render_result = self.render_artifact(lib_result)
        return {
            RES_WRAP: lib_result,
            RES_DJ: dj_result,
            RES_RENDER: render_result,
            RES_LIB: self.get_library()
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
    @abstractmethod
    def setup(self,
              *args) -> None:
        """
        Setup builder.
        """

    @staticmethod
    @abstractmethod
    def filter_constraints(constraints: List[Constraint]
                           ) -> List[Constraint]:
        """
        Filter constraints by library.
        """

    @abstractmethod
    def destroy(self) -> None:
        """
        Destroy builder.
        """
