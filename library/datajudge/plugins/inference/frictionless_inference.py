"""
Frictionless implementation of inference plugin.
"""
from typing import List

import frictionless
from frictionless.schema import Schema

from datajudge.metadata.datajudge_reports import DatajudgeSchema
from datajudge.plugins.base_plugin import PluginBuilder
from datajudge.plugins.inference.inference_plugin import Inference
from datajudge.plugins.utils.plugin_utils import exec_decorator
from datajudge.utils.commons import BASE_FILE_READER, LIBRARY_FRICTIONLESS


class InferencePluginFrictionless(Inference):
    """
    Frictionless implementation of inference plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.resource = None
        self.exec_multiprocess = True

    def setup(
        self, data_reader: "FileReader", resource: "DataResource", exec_args: dict
    ) -> None:
        """
        Set plugin resource.
        """
        self.data_reader = data_reader
        self.resource = resource
        self.exec_args = exec_args

    @exec_decorator
    def infer(self) -> Schema:
        """
        Method that call infer on a resource and return an
        inferred schema.
        """
        data = self.data_reader.fetch_data(self.resource.path)
        schema = Schema.describe(path=data, name=self.resource.name, **self.exec_args)
        return Schema(schema.to_dict())

    @exec_decorator
    def render_datajudge(self, result: "Result") -> DatajudgeSchema:
        """
        Return a DatajudgeSchema.
        """

        exec_err = result.errors
        duration = result.duration

        if exec_err is None:
            inferred_fields = result.artifact.get("fields", [])
            func = lambda x: self._get_fields(x.get("name", ""), x.get("type", ""))
            fields = [func(field) for field in inferred_fields]
        else:
            self.logger.error(f"Execution error {str(exec_err)} for plugin {self._id}")
            fields = []

        return DatajudgeSchema(
            self.get_lib_name(), self.get_lib_version(), duration, fields
        )

    @exec_decorator
    def render_artifact(self, result: "Result") -> List[tuple]:
        """
        Return a frictionless schema to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = dict(result.artifact)
        filename = self._fn_schema.format(f"{LIBRARY_FRICTIONLESS}.json")
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

    def build(
        self, resources: List["DataResource"]
    ) -> List[InferencePluginFrictionless]:
        """
        Build a plugin.
        """
        plugins = []
        for res in resources:
            resource = self._get_resource_deepcopy(res)
            store = self._get_resource_store(resource)
            data_reader = self._get_data_reader(BASE_FILE_READER, store)
            plugin = InferencePluginFrictionless()
            plugin.setup(data_reader, resource, self.exec_args)
            plugins.append(plugin)
        return plugins

    def destroy(self) -> None:
        ...
