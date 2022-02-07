"""
Profiling plugin abstract class module.
"""
# pylint: disable=import-error,invalid-name
import typing
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from typing import Any, List, Optional

if typing.TYPE_CHECKING:
    from datajudge.data import DataResource

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
        self.update_library_info()

    @abstractmethod
    def update_library_info(self) -> None:
        """
        Update metadata about the profiling framework used.
        """

    @abstractmethod
    def parse_profile(self,
                      profile: Any) -> ProfileTuple:
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
