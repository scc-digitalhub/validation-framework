"""
Dummy implementation of profiling plugin.
"""
# pylint: disable=arguments-differ,too-few-public-methods
from __future__ import annotations

import typing
from typing import List

from datajudge.run.plugin.profiling.profiling_plugin import Profiling
from datajudge.run.plugin.base_plugin import PluginBuilder

if typing.TYPE_CHECKING:
    from datajudge import DataResource
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

    def profile(self) -> dict:
        """
        Do nothing.
        """
        return {}

    def produce_profile(self,
                        obj: Result) -> list:
        """
        Parse and prepare a profile to be rendered
        as datajudge artifact.
        """
        return self.get_profile_tuple(None, None, None)

    def render_artifact(self, obj: dict) -> List[tuple]:
        """
        Return a dummy schema to be persisted as artifact.
        """
        artifacts = []
        profile = obj
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
              package: list,
              exec_args: dict,
              *args) -> ProfilePluginDummy:
        """
        Build a plugin.
        """
        plugins = []
        for resource in package:
            plugin = ProfilePluginDummy()
            plugin.setup(resource, exec_args)
            plugins.append(plugin)
        return plugins
