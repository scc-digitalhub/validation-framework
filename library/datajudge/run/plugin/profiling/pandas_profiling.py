"""
Pandas profiling implementation of profiling plugin.
"""
# pylint: disable=import-error,no-name-in-module,arguments-differ,no-member,too-few-public-methods,invalid-name
from __future__ import annotations

import json
import typing
from typing import List, Tuple, Union

import pandas as pd
import pandas_profiling
from frictionless import Resource
from pandas_profiling import ProfileReport

from datajudge.data.datajudge_profile import DatajudgeProfile
from datajudge.run.plugin.profiling.profiling_plugin import Profiling
from datajudge.run.plugin.base_plugin import PluginBuilder
from datajudge.utils.commons import PANDAS_PROFILING
from datajudge.utils.io_utils import write_bytesio
from datajudge.run.plugin.plugin_utils import exec_decorator

if typing.TYPE_CHECKING:
    from datajudge.data.data_resource import DataResource
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
        file_format, pandas_kwargs = self._infer_args(self.resource.tmp_pth)
        df = self._read_df(self.resource.tmp_pth, file_format, **pandas_kwargs)
        profile = ProfileReport(df, **self.exec_args)
        return profile

    @staticmethod
    def _infer_args(data_path: str) -> Tuple[str, dict]:
        """
        Infer with frictionless file format and
        optional arguments for pandas.
        """
        # Possibily, redo this part with simple custom inference
        res = Resource(data_path)
        res.infer()
        res.expand()

        file_format = res.get("format", "csv")
        pandas_args = {
            "sep": res.get("dialect", {}).get("delimiter", ","),
            "encoding": res.get("encoding", "utf-8")
        }
        return file_format, pandas_args

    @staticmethod
    def _read_df(path: Union[str, List[str]],
                 file_format: str,
                 **kwargs: dict) -> pd.DataFrame:
        """
        Read a file into a pandas DataFrame.
        """

        # Check if path is a list of paths
        is_list = isinstance(path, list)

        if file_format == "csv":
            if is_list:
                list_df = [pd.read_csv(i, **kwargs) for i in path]
                df = pd.concat(list_df)
            else:
                df = pd.read_csv(path, **kwargs)
            return df

        if file_format in ["xls", "xlsx", "ods", "odf"]:
            if is_list:
                list_df = [pd.read_excel(i, **kwargs) for i in path]
                df = pd.concat(list_df)
            else:
                df = pd.read_excel(path, **kwargs)
            return df
        
        if file_format == "parquet":
            if is_list:
                list_df = [pd.read_parquet(i) for i in path]
                df = pd.concat(list_df)
            else:
                df = pd.read_parquet(path)
            return df

        raise ValueError("Invalid extension. \
                          Only CSV and XLS supported!")

    @exec_decorator
    def render_datajudge(self, result: Result) -> DatajudgeProfile:
        """
        Return a DatajudgeProfile.
        """
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
        duration = result.duration

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
