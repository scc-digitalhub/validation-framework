"""
Pandas profiling implementation of profiling plugin.
"""
import json
from typing import List

import pandas_profiling
from pandas_profiling import ProfileReport


from datajudge.metadata.datajudge_reports import DatajudgeProfile
from datajudge.plugins.base_plugin import PluginBuilder
from datajudge.plugins.profiling.profiling_plugin import Profiling
from datajudge.plugins.utils.plugin_utils import exec_decorator
from datajudge.utils.commons import (
    LIBRARY_PANDAS_PROFILING,
    PANDAS_DATAFRAME_FILE_READER,
)
from datajudge.utils.io_utils import write_bytesio


# Columns/fields to parse from profile
PROFILE_COLUMNS = ["analysis", "table", "variables"]
PROFILE_FIELDS = [
    "n_distinct",
    "p_distinct",
    "is_unique",
    "n_unique",
    "p_unique",
    "type",
    "hashable",
    "n_missing",
    "n",
    "p_missing",
    "count",
    "memory_size",
]


class ProfilePluginPandasProfiling(Profiling):
    """
    Pandas profiling implementation of profiling plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.resource = None
        self.exec_multiprocess = True

    def setup(
        self,
        data_reader: "NativeReader",
        resource: "DataResource",
        exec_args: dict,
    ) -> None:
        """
        Set plugin resource.
        """
        self.data_reader = data_reader
        self.resource = resource
        self.exec_args = exec_args

    @exec_decorator
    def profile(self) -> ProfileReport:
        """
        Generate pandas_profiling profile.
        """
        data = self.data_reader.fetch_data(self.resource.path)
        profile = ProfileReport(data, lazy=False, **self.exec_args)
        return ProfileReport().loads(profile.dumps())

    @exec_decorator
    def render_datajudge(self, result: "Result") -> DatajudgeProfile:
        """
        Return a DatajudgeProfile.
        """
        exec_err = result.errors
        duration = result.duration

        if exec_err is None:
            # Profile preparation
            json_str = result.artifact.to_json()
            json_str = json_str.replace("NaN", "null")
            full_profile = json.loads(json_str)

            # Short profile args
            args = {k: full_profile.get(k, {}) for k in PROFILE_COLUMNS}

            # Variables overwriting by filtering
            var = args.get("variables", {})
            for key in var:
                args["variables"][key] = {k: var[key][k] for k in PROFILE_FIELDS}

            # Get fields, stats and duration
            fields = args.get("variables", {})
            stats = args.get("table", {})
        else:
            self.logger.error(f"Execution error {str(exec_err)} for plugin {self._id}")
            fields = {}
            stats = {}

        return DatajudgeProfile(
            self.get_lib_name(), self.get_lib_version(), duration, stats, fields
        )

    @exec_decorator
    def render_artifact(self, result: "Result") -> List[tuple]:
        """
        Return a rendered profile ready to be persisted as artifact.
        """
        artifacts = []

        if result.artifact is None:
            _object = {"errors": result.errors}
            filename = self._fn_profile.format(f"{LIBRARY_PANDAS_PROFILING}.json")
            artifacts.append(self.get_render_tuple(_object, filename))
        else:
            string_html = result.artifact.to_html()
            strio_html = write_bytesio(string_html)
            html_filename = self._fn_profile.format(f"{LIBRARY_PANDAS_PROFILING}.html")
            artifacts.append(self.get_render_tuple(strio_html, html_filename))

            string_json = result.artifact.to_json()
            string_json = string_json.replace("NaN", "null")
            strio_json = write_bytesio(string_json)
            json_filename = self._fn_profile.format(f"{LIBRARY_PANDAS_PROFILING}.json")
            artifacts.append(self.get_render_tuple(strio_json, json_filename))

        return artifacts

    @staticmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """
        return pandas_profiling.__name__

    @staticmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """
        return pandas_profiling.__version__


class ProfileBuilderPandasProfiling(PluginBuilder):
    """
    Profile plugin builder.
    """

    def build(
        self, resources: List["DataResource"]
    ) -> List[ProfilePluginPandasProfiling]:
        """
        Build a plugin.
        """
        plugins = []
        for res in resources:
            resource = self._get_resource_deepcopy(res)
            store = self._get_resource_store(resource)
            data_reader = self._get_data_reader(PANDAS_DATAFRAME_FILE_READER, store)
            plugin = ProfilePluginPandasProfiling()
            plugin.setup(data_reader, resource, self.exec_args)
            plugins.append(plugin)
        return plugins

    def destroy(self) -> None:
        """
        Destory plugins.
        """
