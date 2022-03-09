"""
Profiling plugin abstract class module.
"""
# pylint: disable=import-error,invalid-name
from __future__ import annotations

import time
import typing
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from typing import Any

from datajudge.data import DatajudgeProfile
from datajudge.run.plugin.base_plugin import Plugin

if typing.TYPE_CHECKING:
    from datajudge.run.plugin.base_plugin import Result


ProfileTuple = namedtuple("ProfileTuple", ("duration", "stats", "fields"))


class Profiling(Plugin, metaclass=ABCMeta):
    """
    Run plugin that executes profiling over a Resource.
    """

    _fn_profile = "profile_{}"

    @abstractmethod
    def profile(self) -> Any:
        """
        Generate a data profile.
        """

    def execute(self) -> Result:
        """
        Method that call specific execution.
        """
        try:
            self.result.status = self._STATUS_RUNNING
            start = time.perf_counter()
            self.result.artifact = self.profile()
            self.result.time = round(time.perf_counter() - start, 2)
            self.result.status = self._STATUS_FINISHED
        except Exception:
            self.result.status = self._STATUS_ERROR
        return self.result

    @abstractmethod
    def produce_profile(self,
                        obj: Result) -> ProfileTuple:
        """
        Parse and prepare a profile to be rendered
        as datajudge artifact.
        """

    def render_datajudge(self,
                         obj: Result) -> DatajudgeProfile:
        """
        Return a DatajudgeProfile.
        """
        parsed = self.produce_profile(obj)
        return DatajudgeProfile(self.get_lib_name(),
                                self.get_lib_version(),
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
