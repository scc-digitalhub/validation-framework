"""
Base abstract Run Plugin module.
"""
# pylint: disable=too-many-arguments,too-few-public-methods
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from typing import Any, List

from datajudge.utils.config import STATUS_INIT


RenderTuple = namedtuple("RenderTuple", ("object", "filename"))


class Result:
    """
    Simple class to aggregate result of
    plugin operation.
    """
    def __init__(self,
                 libraries: str = None,
                 execution_time: float = None,
                 execution_status: str = None,
                 execution_errors: tuple = None,
                 artifact: Any = None,
                 datajudge_status: str = None,
                 datajudge_errors: tuple = None,
                 datajudge_artifact: Any = None,
                 rendered_status: str = None,
                 rendered_errors: tuple = None,
                 rendered_artifact: Any = None) -> None:
        self.libraries = libraries
        self.execution_time = execution_time
        self.execution_status = execution_status
        self.execution_errors = execution_errors
        self.artifact = artifact
        self.datajudge_status = datajudge_status
        self.datajudge_errors = datajudge_errors
        self.datajudge_artifact = datajudge_artifact
        self.rendered_status = rendered_status
        self.rendered_errors = rendered_errors
        self.rendered_artifact = rendered_artifact


class Plugin(metaclass=ABCMeta):
    """
    Base plugin abstract class.
    """

    def __init__(self) -> None:
        self.lib_name = self.get_lib_name()
        self.lib_version = self.get_lib_version()
        self.result = Result(execution_status=STATUS_INIT)

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
