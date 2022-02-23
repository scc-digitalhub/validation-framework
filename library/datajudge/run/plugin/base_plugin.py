"""
Base abstract Run Plugin module.
"""

from abc import ABCMeta, abstractmethod
from collections import namedtuple
from typing import Any, List, Optional

from datajudge.run.plugin.results_registry import ResultsRegistry


RenderTuple = namedtuple("RenderTuple", ("object", "filename"))


class Plugin(metaclass=ABCMeta):
    
    def __init__(self) -> None:
        self.lib_name = None
        self.lib_version = None
        self.registry = ResultsRegistry()
        self.update_library_info()

    @abstractmethod
    def update_library_info(self) -> None:
        """
        Update run's info about the validation framework used.
        """

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        """
        Execute main plugin operation.
        """

    @abstractmethod
    def render_datajudge(self, *args, **kwargs) -> Any:
        """
        Return a DataJudge report.
        """

    @abstractmethod
    def render_artifact(self, obj: Any) -> List[tuple]:
        """
        Return a rendered report ready to be persisted as artifact.
        """

    def get_args(self,
                 args: Optional[dict] = None) -> dict:
        """
        Return keywords arguments for execution.
        """
        if args is not None:
            return args.get(self.lib_name, {})
        return {}

    @staticmethod
    def get_render_tuple(obj: Any, filename: str) -> RenderTuple:
        """
        Return a RenderTuple.
        """
        return RenderTuple(obj, filename)

    def libraries(self) -> dict:
        """
        Get libraries infos.
        """
        return {
                "libName": self.lib_name,
                "libVersion": self.lib_version
        }
