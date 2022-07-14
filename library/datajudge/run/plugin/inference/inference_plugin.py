"""
Inference plugin abstract class module.
"""

from abc import ABCMeta, abstractmethod
from typing import Any

from datajudge.run.plugin.base_plugin import Plugin
from datajudge.utils.commons import (RES_WRAP, RES_DJ,
                                     RES_RENDER, RES_LIB)


class Inference(Plugin, metaclass=ABCMeta):
    """
    Run plugin that executes inference over a Resource.
    """

    _fn_schema = "schema_{}"

    def execute(self) -> dict:
        """
        Method that call specific execution.
        """
        self.logger.info(
            f"Execute inference: plugin {self.lib_name} {self._id}, resource {self.resource.name}")
        lib_result = self.infer()
        self.logger.info(
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
    def infer(self) -> Any:
        """
        Inference method for schema.
        """
