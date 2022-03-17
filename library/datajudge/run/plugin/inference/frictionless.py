"""
Frictionless implementation of inference plugin.
"""
# pylint: disable=import-error,no-name-in-module,arguments-differ,no-member,too-few-public-methods
from __future__ import annotations

import typing
from typing import List

import frictionless
from frictionless import describe_schema
from frictionless.schema import Schema

from datajudge.run.plugin.base_plugin import PluginBuilder
from datajudge.run.plugin.inference.inference_plugin import Inference

if typing.TYPE_CHECKING:
    from datajudge import DataResource
    from datajudge.run.plugin.base_plugin import Result
    from datajudge.run.plugin.inference.inference_plugin import SchemaTuple


class InferencePluginFrictionless(Inference):
    """
    Frictionless implementation of inference plugin.
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

    def infer(self) -> Schema:
        """
        Method that call infer on a resource and return an
        inferred schema.
        """
        return describe_schema(path=self.resource.tmp_pth,
                               name=self.resource.name,
                               **self.exec_args)

    def produce_schema(self,
                       obj: Result) -> List[SchemaTuple]:
        """
        Method that produce a datajudge schema.
        """

        field_infer = obj.artifact.get("fields", [])
        duration = obj.time

        dj_schema_fields = []
        if field_infer:
            for field in field_infer:
                dj_schema_fields.append({
                    "name": field.get("name", ""),
                    "type": field.get("type", "")
                    })
        else:
            dj_schema_fields = [{"name": None, "type": None}]

        return self.get_schema_tuple(duration, dj_schema_fields)

    def render_artifact(self, obj: Schema) -> List[tuple]:
        """
        Return a frictionless schema to be persisted as artifact.
        """
        artifacts = []
        schema = dict(obj)
        filename = self._fn_schema.format("frictionless.json")
        artifacts.append(self.get_render_tuple(schema, filename))
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


class InferenceBuilderFrictionless(PluginBuilder):
    """
    Inference plugin builder.
    """

    def build(self,
              package: list,
              exec_args: dict,
              *args) -> InferencePluginFrictionless:
        """
        Build a plugin.
        """
        plugins = []
        for resource in package:
            plugin = InferencePluginFrictionless()
            plugin.setup(resource,
                         exec_args)
            plugins.append(plugin)
        return plugins
