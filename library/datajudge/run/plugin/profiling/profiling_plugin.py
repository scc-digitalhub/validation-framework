"""
Profiling plugin abstract class module.
"""
# pylint: disable=import-error,invalid-name
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from typing import Any, Optional

from datajudge.data import DatajudgeProfile
from datajudge.run.plugin.base_plugin import Plugin


ProfileTuple = namedtuple("ProfileTuple", ("duration", "stats", "fields"))


class Profiling(Plugin, metaclass=ABCMeta):
    """
    Run plugin that executes profiling over a Resource.
    """

    _fn_profile = "profile_{}"

    @abstractmethod
    def parse_profile(self,
                      profile: Any,
                      res_name: str) -> tuple:
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

    def execute(self, *args, **kwargs) -> Any:
        """
        Execute plugin main operation.
        """
        return self.profile(*args, **kwargs)

    def render_datajudge(self,
                         profile: Any,
                         res_name: str) -> DatajudgeProfile:
        """
        Return a DatajudgeProfile.
        """
        parsed = self.parse_profile(profile, res_name)
        return DatajudgeProfile(self.lib_name,
                                self.lib_version,
                                parsed.duration,
                                parsed.stats,
                                parsed.fields)

    @staticmethod
    def get_profile_tuple(duration: float,
                          stats: Any,
                          fields: Any) -> ProfileTuple:
        """
        Return ProfileTuple.
        """
        return ProfileTuple(duration, stats, fields)

