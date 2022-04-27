"""
Dummy implementation of profiling plugin.
"""
# pylint: disable=arguments-differ,too-few-public-methods
from __future__ import annotations

import typing
from typing import List

from datajudge.data.datajudge_profile import DatajudgeProfile
from datajudge.run.plugin.profiling.profiling_plugin import Profiling
from datajudge.run.plugin.base_plugin import PluginBuilder
from datajudge.utils.commons import DUMMY
from datajudge.run.plugin.plugin_utils import exec_decorator

if typing.TYPE_CHECKING:
    from datajudge.data.data_resource import DataResource
    from datajudge.run.plugin.base_plugin import Result


class ProfilePluginDummy(Profiling):
    """
    Dummy implementation of profiling plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.resource = None
        self.exec_args = None

    def setup(self,
              resource: DataResource,
              exec_args: dict) -> None:
        """
        Set plugin resource.
        """
        self.resource = resource
        self.exec_args = exec_args

    @exec_decorator
    def profile(self) -> dict:
        """
        Do nothing.
        """
        return {}

    @exec_decorator
    def render_datajudge(self, result: Result) -> DatajudgeProfile:
        """
        Return a DatajudgeProfile.
        """
        return DatajudgeProfile(self.get_lib_name(),
                                self.get_lib_version(),
                                None,
                                None,
                                None)

    @exec_decorator
    def render_artifact(self, result: Result) -> List[tuple]:
        """
        Return a dummy schema to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = dict(result.artifact)
        filename = self._fn_profile.format(f"{DUMMY}.json")
        artifacts.append(self.get_render_tuple(_object, filename))
        return artifacts

    @staticmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """
        return None

    @staticmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """
        return None


class ProfileBuilderDummy(PluginBuilder):
    """
    Profile plugin builder.
    """
    def build(self,
              resources: List[DataResource]
              ) -> List[ProfilePluginDummy]:
        """
        Build a plugin.
        """
        plugins = []
        plugin = ProfilePluginDummy()
        plugin.setup(resources, self.exec_args)
        plugins.append(plugin)
        return plugins
