"""
Inference plugin abstract class module.
"""

from abc import ABCMeta, abstractmethod
from typing import Any

from datajudge.plugins.base_plugin import Plugin
from datajudge.utils.commons import (
    RESULT_DATAJUDGE,
    RESULT_LIBRARY,
    RESULT_RENDERED,
    RESULT_WRAPPED,
)


class Inference(Plugin, metaclass=ABCMeta):
    """
    Run plugin that executes inference over a Resource.
    """

    _fn_schema = "schema_{}"

    def execute(self) -> dict:
        """
        Method that call specific execution.
        """
        plugin = f"Plugin: {self.lib_name} {self._id};"
        self.logger.info(f"Execute inference - {plugin}")
        lib_result = self.infer()
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
    def infer(self) -> Any:
        """
        Inference method for schema.
        """

    @staticmethod
    def _get_fields(name: str = None, type_: str = None) -> dict:
        """
        Return a common field structure.
        """
        return {"name": name, "type": type_}
