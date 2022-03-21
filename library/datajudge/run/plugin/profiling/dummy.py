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
from datajudge.utils.utils import exec_decorator

if typing.TYPE_CHECKING:
    from datajudge.data.data_resource import DataResource


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
    def render_datajudge(self) -> DatajudgeProfile:
        """
        Return a DatajudgeProfile.
        """
        return DatajudgeProfile(self.get_lib_name(),
                                self.get_lib_version(),
                                None,
                                None,
                                None)

    @exec_decorator
    def render_artifact(self) -> List[tuple]:
        """
        Return a dummy schema to be persisted as artifact.
        """
        artifacts = []
        profile = self.result.artifact
        filename = self._fn_profile.format("dummy.json")
        artifacts.append(self.get_render_tuple(profile, filename))
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
              resources: list,
              exec_args: dict,
              *args) -> ProfilePluginDummy:
        """
        Build a plugin.
        """
        plugins = []
        for resource in resources:
            plugin = ProfilePluginDummy()
            plugin.setup(resource, exec_args)
            plugins.append(plugin)
        return plugins
