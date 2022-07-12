"""
Pandas profiling implementation of profiling plugin.
"""
# pylint: disable=import-error,no-name-in-module,arguments-differ,no-member,too-few-public-methods,invalid-name
from __future__ import annotations

import json
import typing
from typing import List

import pandas_profiling
from pandas_profiling import ProfileReport

from datajudge.data import DatajudgeProfile
from datajudge.run.plugin.base_plugin import PluginBuilder
from datajudge.run.plugin.utils.plugin_utils import exec_decorator
from datajudge.run.plugin.profiling.profiling_plugin import Profiling
from datajudge.utils.commons import PANDAS_PROFILING
from datajudge.run.plugin.utils.dataframe_reader import DataFrameReader
from datajudge.utils.io_utils import write_bytesio

if typing.TYPE_CHECKING:
    from datajudge.data import DataResource
    from datajudge.run.plugin.base_plugin import Result


# Columns/fields to parse from profile
PROFILE_COLUMNS = ["analysis", "table", "variables"]
PROFILE_FIELDS = ["n_distinct", "p_distinct", "is_unique",
                  "n_unique", "p_unique", "type", "hashable",
                  "n_missing", "n", "p_missing", "count",
                  "memory_size"]


class ProfilePluginPandasProfiling(Profiling):
    """
    Pandas profiling implementation of profiling plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.resource = None
        self.exec_args = None
        self.exec_multiprocess = True

    def setup(self,
              resource: DataResource,
              exec_args: dict) -> None:
        """
        Set plugin resource.
        """
        self.resource = resource
        self.exec_args = exec_args

    @exec_decorator
    def profile(self) -> ProfileReport:
        """
        Generate pandas_profiling profile.
        """
        df = DataFrameReader(self.resource.tmp_pth).read_df()
        profile = ProfileReport(df, lazy=False, **self.exec_args)
        profile = ProfileReport().loads(profile.dumps())
        return profile

    @exec_decorator
    def render_datajudge(self, result: Result) -> DatajudgeProfile:
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
            args = {
                k: full_profile.get(k, {}) for k in PROFILE_COLUMNS
            }

            # Variables overwriting by filtering
            var = args.get("variables", {})
            for key in var:
                args["variables"][key] = {
                    k: var[key][k] for k in PROFILE_FIELDS
                }

            # Get fields, stats and duration
            fields = args.get("variables", {})
            stats = args.get("table", {})
        else:
            self.logger.error(f"Execution error {str(exec_err)} for plugin {self._id}")
            fields = None
            stats = None

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
            filename = self._fn_profile.format(f"{PANDAS_PROFILING}.json")
            artifacts.append(self.get_render_tuple(_object, filename))
        else:
            string_html = result.artifact.to_html()
            strio_html = write_bytesio(string_html)
            html_filename = self._fn_profile.format(f"{PANDAS_PROFILING}.html")
            artifacts.append(self.get_render_tuple(strio_html, html_filename))

            string_json = result.artifact.to_json()
            string_json = string_json.replace("NaN", "null")
            strio_json = write_bytesio(string_json)
            json_filename = self._fn_profile.format(f"{PANDAS_PROFILING}.json")
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
    def build(self,
              resources: List[DataResource]
              ) -> List[ProfilePluginPandasProfiling]:
        """
        Build a plugin.
        """
        plugins = []
        for res in resources:
            resource = self.fetch_resource(res)
            plugin = ProfilePluginPandasProfiling()
            plugin.setup(resource, self.exec_args)
            plugins.append(plugin)
        return plugins

    def destroy(self) -> None:
        """
        Destory plugins.
        """

