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
from datajudge.utils.commons import FRICTIONLESS
from datajudge.utils.io_utils import write_bytesio
from datajudge.run.plugin.plugin_utils import exec_decorator

if typing.TYPE_CHECKING:
    from datajudge.data.data_resource import DataResource
    from datajudge.run.plugin.base_plugin import Result


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
    def render_datajudge(self, result: Result) -> DatajudgeProfile:
        """
        Return a DatajudgeProfile.
        """
        rep = result.artifact.to_dict()
        duration = result.duration
        fields = rep.get("schema", {}).get("fields")
        stats = {k: v for k, v in rep.items() if k != "schema"}
        return DatajudgeProfile(self.get_lib_name(),
                                self.get_lib_version(),
                                duration,
                                stats,
                                fields)

    @exec_decorator
    def render_artifact(self, result: Result) -> List[tuple]:
        """
        Return a rendered profile ready to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = write_bytesio(result.artifact.to_json())
        filename = self._fn_profile.format(f"{FRICTIONLESS}.json")
        artifacts.append(self.get_render_tuple(_object, filename))
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
              resources: List[DataResource]
              ) -> List[ProfilePluginFrictionless]:
        """
        Build a plugin.
        """
        plugins = []
        for res in resources:
            resource = self.fetch_resource(res)
            plugin = ProfilePluginFrictionless()
            plugin.setup(resource, self.exec_args)
            plugins.append(plugin)
        return plugins
