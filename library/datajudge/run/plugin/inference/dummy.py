"""
Dummy implementation of inference plugin.
"""
# pylint: disable=arguments-differ,too-few-public-methods
from __future__ import annotations

import typing
from typing import List

from datajudge.data import DatajudgeSchema
from datajudge.run.plugin.inference.inference_plugin import Inference
from datajudge.run.plugin.base_plugin import PluginBuilder
from datajudge.utils.commons import DUMMY
from datajudge.run.plugin.plugin_utils import exec_decorator

if typing.TYPE_CHECKING:
    from datajudge.data.data_resource import DataResource
    from datajudge.run.plugin.base_plugin import Result


class InferencePluginDummy(Inference):
    """
    Dummy implementation of inference plugin.
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
    def infer(self) -> dict:
        """
        Do nothing.
        """
        return {}

    @exec_decorator
    def render_datajudge(self, result: Result) -> DatajudgeSchema:
        """
        Return a DatajudgeSchema.
        """
        return DatajudgeSchema(self.get_lib_name(),
                               self.get_lib_version(),
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
        filename = self._fn_schema.format(f"{DUMMY}.json")
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


class InferenceBuilderDummy(PluginBuilder):
    """
    Inference plugin builder.
    """
    def build(self,
              resources: List[DataResource]
              ) -> InferencePluginDummy:
        """
        Build a plugin.
        """
        plugins = []
        for resource in resources:
            plugin = InferencePluginDummy()
            plugin.setup(resource, self.exec_args)
            plugins.append(plugin)
        return plugins
