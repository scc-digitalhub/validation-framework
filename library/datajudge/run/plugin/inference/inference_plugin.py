"""
Inference plugin abstract class module.
"""

from abc import ABCMeta, abstractmethod
from typing import Any

from datajudge.run.plugin.base_plugin import Plugin
from datajudge.utils.commons import (RESULT_DATAJUDGE, RESULT_LIBRARY,
                                     RESULT_RENDERED, RESULT_WRAPPED)


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
            f"Execute inference: plugin {self.lib_name} {self._id}")
        lib_result = self.infer()
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
    def infer(self) -> Any:
        """
        Inference method for schema.
        """
