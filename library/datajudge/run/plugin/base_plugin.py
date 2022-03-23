"""
Base abstract Run Plugin module.
"""
# pylint: disable=too-many-arguments,too-few-public-methods
from __future__ import annotations

import typing
from abc import ABCMeta, abstractmethod
from typing import Any, List

from datajudge.run.plugin.plugin_utils import RenderTuple

if typing.TYPE_CHECKING:
    from datajudge.run.plugin.plugin_utils import Result


class Plugin(metaclass=ABCMeta):
    """
    Base plugin abstract class.
    """

    def __init__(self) -> None:
        self.lib_name = self.get_lib_name()
        self.lib_version = self.get_lib_version()

    @abstractmethod
    def setup(self, *args, **kwargs) -> None:
        """
        Configure a plugin.
        """

    @abstractmethod
    def execute(self) -> dict:
        """
        Execute main plugin operation.
        """

    @abstractmethod
    def render_datajudge(self, obj: Result) -> Result:
        """
        Produce datajudge output.
        """

    @abstractmethod
    def render_artifact(self, obj: Result) -> Result:
        """
        Render an artifact to be persisted.
        """

    @staticmethod
    def get_render_tuple(obj: Any, filename: str) -> RenderTuple:
        """
        Return a RenderTuple.
        """
        return RenderTuple(obj, filename)

    @staticmethod
    @abstractmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """

    @staticmethod
    @abstractmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """

    def get_library(self) -> dict:
        """
        Get library info.
        """
        return {
            "libraryName": self.get_lib_name(),
            "libraryVersion": self.get_lib_version()
        }


class PluginBuilder:
    """
    Abstract PluginBuilder class.
    """

    def __init__(self,
                 exec_args: dict) -> None:
        self.exec_args = exec_args

    @abstractmethod
    def build(self, *args, **kwargs) -> List[Plugin]:
        """
        Build a list of plugin.
        """
