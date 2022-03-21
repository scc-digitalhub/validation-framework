"""
Frictionless implementation of profiling plugin.
"""
# pylint: disable=import-error,no-name-in-module,arguments-differ,no-member,too-few-public-methods
from __future__ import annotations

import typing
from typing import List

import frictionless
from frictionless import Resource

from datajudge.data.datajudge_profile import DatajudgeProfile
from datajudge.run.plugin.profiling.profiling_plugin import Profiling
from datajudge.run.plugin.base_plugin import PluginBuilder
from datajudge.utils.io_utils import write_bytesio
from datajudge.utils.utils import exec_decorator

if typing.TYPE_CHECKING:
    from datajudge.data.data_resource import DataResource


class ProfilePluginFrictionless(Profiling):
    """
    Frictionless implementation of profiling plugin.
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
    def profile(self) -> Resource:
        """
        Do nothing.
        """
        profile = Resource(self.resource.tmp_pth,
                           **self.exec_args)
        profile.infer()
        profile.expand()
        return profile

    @exec_decorator
    def render_datajudge(self) -> DatajudgeProfile:
        """
        Return a DatajudgeProfile.
        """
        rep = self.result.artifact.to_dict()
        duration = self.result.execution_time
        fields = rep.get("schema", {}).get("fields")
        try:
            rep.pop("schema")
        except KeyError:
            pass
        stats = rep
        return DatajudgeProfile(self.get_lib_name(),
                                self.get_lib_version(),
                                duration,
                                stats,
                                fields)

    @exec_decorator
    def render_artifact(self) -> List[tuple]:
        """
        Return a rendered profile ready to be persisted as artifact.
        """
        artifacts = []
        profile = write_bytesio(self.result.artifact.to_json())
        filename = self._fn_profile.format("frictionless.json")
        artifacts.append(self.get_render_tuple(profile, filename))
        return artifacts

    @staticmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """
        return frictionless.__name__

    @staticmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """
        return frictionless.__version__


class ProfileBuilderFrictionless(PluginBuilder):
    """
    Profile plugin builder.
    """

    def build(self,
              resources: list
              ) -> ProfilePluginFrictionless:
        """
        Build a plugin.
        """
        plugins = []
        for resource in resources:
            plugin = ProfilePluginFrictionless()
            plugin.setup(resource, self.exec_args)
            plugins.append(plugin)
        return plugins
