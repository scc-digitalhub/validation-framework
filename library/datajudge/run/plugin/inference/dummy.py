"""
Dummy implementation of inference plugin.
"""
# pylint: disable=arguments-differ,too-few-public-methods
from __future__ import annotations

import typing
from typing import List

from datajudge.run.plugin.inference.inference_plugin import Inference
from datajudge.run.plugin.base_plugin import PluginBuilder

if typing.TYPE_CHECKING:
    from datajudge import DataResource
    from datajudge.run.plugin.base_plugin import Result
    from datajudge.run.plugin.inference.inference_plugin import SchemaTuple


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

    def infer(self) -> dict:
        """
        Do nothing.
        """
        return {}

    def produce_schema(self, obj: Result) -> List[SchemaTuple]:
        """
        Do nothing.
        """
        return [self.get_schema_tuple(None, None)]

    def render_artifact(self, obj: dict) -> List[tuple]:
        """
        Return a dummy schema to be persisted as artifact.
        """
        artifacts = []
        schema = obj
        filename = self._fn_schema.format("dummy.json")
        artifacts.append(self.get_render_tuple(schema, filename))
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
              package: list,
              exec_args: dict,
              *args) -> InferencePluginDummy:
        """
        Build a plugin.
        """
        plugins = []
        for resource in package:
            plugin = InferencePluginDummy()
            plugin.setup(resource, exec_args)
            plugins.append(plugin)
        return plugins
