"""
Profiling plugin abstract class module.
"""
from abc import ABCMeta, abstractmethod
from typing import Any

from datajudge.plugins.base_plugin import Plugin
from datajudge.utils.commons import (
    RESULT_WRAPPED,
    RESULT_DATAJUDGE,
    RESULT_RENDERED,
    RESULT_LIBRARY,
)


class Profiling(Plugin, metaclass=ABCMeta):
    """
    Run plugin that executes profiling over a Resource.
    """

    _fn_profile = "profile_{}"

    def execute(self) -> dict:
        """
        Method that call specific execution.
        """
        plugin = f"Plugin: {self.lib_name} {self._id};"
        self.logger.info(f"Execute profiling - {plugin}")
        lib_result = self.profile()
        self.logger.info(f"Render report - {plugin}")
        dj_result = self.render_datajudge(lib_result)
        self.logger.info(f"Render artifact - {plugin}")
        render_result = self.render_artifact(lib_result)
        return {
            RESULT_WRAPPED: lib_result,
            RESULT_DATAJUDGE: dj_result,
            RESULT_RENDERED: render_result,
            RESULT_LIBRARY: self.get_library(),
        }

    @abstractmethod
    def profile(self) -> Any:
        """
        Generate a data profile.
        """
