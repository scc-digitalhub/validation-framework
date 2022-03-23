"""
Profiling plugin abstract class module.
"""
# pylint: disable=import-error,invalid-name
from __future__ import annotations

import typing
from abc import ABCMeta, abstractmethod
from typing import Any, List

from datajudge.run.plugin.base_plugin import Plugin
from datajudge.utils.commons import (RES_WRAP, RES_DJ,
                                     RES_RENDER, RES_LIB)

if typing.TYPE_CHECKING:
    from datajudge.run.plugin.base_plugin import Result


class Profiling(Plugin, metaclass=ABCMeta):
    """
    Run plugin that executes profiling over a Resource.
    """

    _fn_profile = "profile_{}"

    def execute(self) -> dict:
        """
        Method that call specific execution.
        """
        lib_result = self.profile()
        dj_result = self.render_datajudge(lib_result)
        render_result = self.render_artifact(lib_result)
        return {
            RES_WRAP: lib_result,
            RES_DJ: dj_result,
            RES_RENDER: render_result,           
            RES_LIB: self.get_library()
        }

    @abstractmethod
    def profile(self) -> Any:
        """
        Generate a data profile.
        """
