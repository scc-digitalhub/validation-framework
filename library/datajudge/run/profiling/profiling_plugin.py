"""
Profiling plugin abstract class module.
"""
# pylint: disable=import-error,invalid-name
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from typing import Any, List, Optional

from datajudge.run.results_registry import ResultsRegistry


ProfileTuple = namedtuple("ProfileTuple",
                          ("duration", "stats", "fields"))
RenderTuple = namedtuple("RenderTuple",
                         ("object", "filename"))


class Profiling(metaclass=ABCMeta):
    """
    Run plugin that executes profiling over a Resource.
    """

    def __init__(self) -> None:
        self.lib_name = None
        self.lib_version = None
        self.registry = ResultsRegistry()
        self.update_library_info()

    @abstractmethod
    def update_library_info(self) -> None:
        """
        Update metadata about the profiling framework used.
        """

    @abstractmethod
    def parse_profile(self,
                      profile: Any,
                      res_name: str) -> ProfileTuple:
        """
        Parse a data profile.
        """

    @abstractmethod
    def validate_profile(self,
                         profile: Optional[Any] = None
                         ) -> None:
        """
        Validate a data profile.
        """

    @abstractmethod
    def profile(self,
                res_name: str,
                data_path: str,
                resource: Any,
                profiler_kwargs: Optional[dict] = None
                ) -> Any:
        """
        Generate a data profile.
        """

    @abstractmethod
    def render_object(self,
                      obj: Any) -> List[RenderTuple]:
        """
        Return a rendered profile ready to be persisted as artifact.
        """

    # Getters

    def get_lib_name(self) -> str:
        return self.lib_name
    
    def get_lib_version(self) -> str:
        return self.lib_version
    
    def get_lib(self) -> dict:
        return {
                "libName": self.lib_name,
                "libVersion": self.lib_version
        }
