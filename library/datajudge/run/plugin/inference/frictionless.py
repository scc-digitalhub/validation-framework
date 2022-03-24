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

from datajudge.data import DatajudgeSchema
from datajudge.run.plugin.base_plugin import PluginBuilder
from datajudge.run.plugin.inference.inference_plugin import Inference
from datajudge.utils.commons import FRICTIONLESS
from datajudge.run.plugin.plugin_utils import exec_decorator

if typing.TYPE_CHECKING:
    from datajudge.data.data_resource import DataResource
    from datajudge.run.plugin.base_plugin import Result


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

    @exec_decorator
    def infer(self) -> Schema:
        """
        Method that call infer on a resource and return an
        inferred schema.
        """
        return describe_schema(path=self.resource.tmp_pth,
                               name=self.resource.name,
                               **self.exec_args)

    @exec_decorator
    def render_datajudge(self, result: Result) -> DatajudgeSchema:
        """
        Return a DatajudgeSchema.
        """

        field_infer = result.artifact.get("fields", [])
        duration = result.duration

        dj_schema_fields = []
        if field_infer:
            for field in field_infer:
                dj_schema_fields.append({
                    "name": field.get("name", ""),
                    "type": field.get("type", "")
                    })
        else:
            dj_schema_fields = [{"name": None, "type": None}]

        return DatajudgeSchema(self.get_lib_name(),
                               self.get_lib_version(),
                               duration,
                               dj_schema_fields)

    @exec_decorator
    def render_artifact(self, result: Result) -> List[tuple]:
        """
        Return a frictionless schema to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = dict(result.artifact)
        filename = self._fn_schema.format(f"{FRICTIONLESS}.json")
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


class InferenceBuilderFrictionless(PluginBuilder):
    """
    Inference plugin builder.
    """

    def build(self,
              resources: List[DataResource]
              ) -> InferencePluginFrictionless:
        """
        Build a plugin.
        """
        plugins = []
        for resource in resources:
            plugin = InferencePluginFrictionless()
            plugin.setup(resource, self.exec_args)
            plugins.append(plugin)
        return plugins
