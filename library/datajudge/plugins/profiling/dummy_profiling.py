"""
Dummy implementation of profiling plugin.
"""
# pylint: disable=unused-argument
from typing import List

from datajudge.metadata.datajudge_reports import DatajudgeProfile
from datajudge.plugins.base_plugin import PluginBuilder
from datajudge.plugins.profiling.profiling_plugin import Profiling
from datajudge.plugins.utils.plugin_utils import exec_decorator
from datajudge.utils.commons import GENERIC_DUMMY, LIBRARY_DUMMY


class ProfilePluginDummy(Profiling):
    """
    Dummy implementation of profiling plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.resource = None

    def setup(self,
              resource: "DataResource",
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
    def render_datajudge(self, result: "Result") -> DatajudgeProfile:
        """
        Return a DatajudgeProfile.
        """
        return DatajudgeProfile(self.get_lib_name(),
                                self.get_lib_version(),
                                None,
                                None,
                                None)

    @exec_decorator
    def render_artifact(self, result: "Result") -> List[tuple]:
        """
        Return a dummy schema to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = dict(result.artifact)
        filename = self._fn_profile.format(f"{GENERIC_DUMMY}.json")
        artifacts.append(self.get_render_tuple(_object, filename))
        return artifacts

    @staticmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """
        return LIBRARY_DUMMY

    @staticmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """
        return LIBRARY_DUMMY


class ProfileBuilderDummy(PluginBuilder):
    """
    Profile plugin builder.
    """

    def build(self,
              resources: List["DataResource"]
              ) -> List[ProfilePluginDummy]:
        """
        Build a plugin.
        """
        plugins = []
        plugin = ProfilePluginDummy()
        plugin.setup(None, self.exec_args)
        plugins.append(plugin)
        return plugins

    def destroy(self) -> None:
        """
        Destory plugins.
        """
