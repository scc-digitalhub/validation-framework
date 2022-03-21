"""
Inference plugin abstract class module.
"""
# pylint: disable=import-error,invalid-name
from __future__ import annotations

import typing
from abc import ABCMeta, abstractmethod
from typing import Any

from datajudge.run.plugin.base_plugin import Plugin
from datajudge.utils.config import STATUS_RUNNING

if typing.TYPE_CHECKING:
    from datajudge.run.plugin.base_plugin import Result


class Inference(Plugin, metaclass=ABCMeta):
    """
    Run plugin that executes inference over a Resource.
    """

    _fn_schema = "schema_{}"

    def execute(self) -> Result:
        """
        Method that call specific execution.
        """
        self.result.libraries = self.get_library()

        self.result.execution_status = STATUS_RUNNING
        self.result.artifact, \
            self.result.execution_status, \
                self.result.execution_errors, \
                    self.result.execution_time = self.infer()

        self.result.datajudge_status = STATUS_RUNNING
        self.result.datajudge_artifact, \
            self.result.datajudge_status, \
                self.result.datajudge_errors, _ = self.render_datajudge()

        self.result.datajudge_status = STATUS_RUNNING                    
        self.result.rendered_artifact, \
            self.result.rendered_status, \
                self.result.rendered_errors, _ = self.render_artifact()

        return self.result

    @abstractmethod
    def infer(self) -> Any:
        """
        Inference method for schema.
        """
