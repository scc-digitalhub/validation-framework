"""
Base abstract Run Plugin module.
"""
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from typing import Any, List

import datajudge


RenderTuple = namedtuple("RenderTuple", ("object", "filename"))


class Result:
    """
    Simple class to aggregate result of
    plugin operation.
    """
    def __init__(self,
                 artifact: Any = None,
                 datajudge_doc: Any = None,
                 status: str = None,
                 time: float = None) -> None:
        self.artifact = artifact
        self.datajudge_doc = datajudge_doc
        self.status = status
        self.time = time


class Plugin(metaclass=ABCMeta):
    """
    Base plugin abstract class.
    """

    _STATUS_INIT = "created"
    _STATUS_RUNNING = "executing"
    _STATUS_FINISHED = "finished"
    _STATUS_ERROR = "error"

    def __init__(self) -> None:
        self.lib_name = self.get_lib_name()
        self.lib_version = self.get_lib_version()
        self.result = Result(status=self._STATUS_INIT)

    @abstractmethod
    def setup(self, *args, **kwargs) -> None:
        """
        Configure a plugin.
        """

    @abstractmethod
    def execute(self) -> Result:
        """
        Execute main plugin operation.
        """

    def get_result(self) -> Result:
        """
        Return status of the execution.
        """
        return self.result

    @abstractmethod
    def render_datajudge(self, obj: Result) -> Any:
        """
        Produce datajudge output.
        """

    @abstractmethod
    def render_artifact(self, obj: Result) -> Any:
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

    @abstractmethod
    def build(self, *args, **kwargs) -> List[Plugin]:
        """
        Build a list of plugin.
        """
