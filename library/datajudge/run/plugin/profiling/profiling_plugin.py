"""
Profiling plugin abstract class module.
"""

from abc import ABCMeta, abstractmethod
from typing import Any

from datajudge.run.plugin.base_plugin import Plugin
from datajudge.utils.commons import (RES_WRAP, RES_DJ,
                                     RES_RENDER, RES_LIB)


class Profiling(Plugin, metaclass=ABCMeta):
    """
    Run plugin that executes profiling over a Resource.
    """

    _fn_profile = "profile_{}"

    def execute(self) -> dict:
        """
        Method that call specific execution.
        """
        self.logger.log(9,
            f"Execute profiling: plugin {self.lib_name} {self._id}, resource {self.resource.name}")
        lib_result = self.profile()
        self.logger.log(9,
            f"Render datajudge result: plugin {self.lib_name} {self._id}")
        dj_result = self.render_datajudge(lib_result)
        self.logger.info(f"Render artifact: plugin {self.lib_name} {self._id}")
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
