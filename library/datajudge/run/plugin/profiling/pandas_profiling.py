"""
Pandas profiling implementation of profiling plugin.
"""
# pylint: disable=import-error,invalid-name
import json
from typing import List, Optional, Tuple, Union

import pandas as pd
import pandas_profiling
from frictionless import Resource
from pandas_profiling import ProfileReport

from datajudge.run.plugin.profiling.profiling_plugin import Profiling
from datajudge.utils.io_utils import write_bytesio
from datajudge.utils.utils import time_to_sec


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

    def update_library_info(self) -> None:
        """
        Update run's info about the validation framework used.
        """
        self.lib_name = pandas_profiling.__name__
        self.lib_version = pandas_profiling.__version__

    def parse_profile(self,
                      profile: ProfileReport,
                      res_name: str) -> tuple:
        """
        Parse the profile generated by pandas profiling.
        """

        # Profile preparation
        json_str = profile.to_json()
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
        duration = self.registry.get_time(res_name)

        return self.get_profile_tuple(duration, stats, fields)

    def validate_profile(self, profile: ProfileReport) -> None:
        """
        Validate the profile.
        """
        if not isinstance(profile, ProfileReport):
            raise TypeError("Expected pandas_profiling Profile!")

    def profile(self,
                res_name: str,
                data_path: str,
                exec_args: dict
                ) -> ProfileReport:
        """
        Generate pandas_profiling profile.

        Parameters
        ----------
        **exec_args : dict, default = None
            Parameters for pandas_profiling.ProfileReport.

        """
        file_format, pandas_kwargs = self._infer_args(data_path)
        df = self._read_df(data_path,
                           file_format,
                           **pandas_kwargs)
        profile = ProfileReport(df, **exec_args)

        time = json.loads(profile.to_json())\
                   .get("analysis", {})\
                   .get("duration")
        time = time_to_sec(time)

        self.registry.add_result(res_name, profile, time)

        return profile

    def get_outcome(self, obj: ProfileReport) -> str:
        """
        Return status of the execution.
        """
        if obj is not None:
            return self._VALID_STATUS
        return self._INVALID_STATUS

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

        raise ValueError("Invalid extension.",
                         " Only CSV and XLS supported!")

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

    def render_artifact(self,
                        obj: ProfileReport) -> List[tuple]:
        """
        Return a rendered profile ready to be persisted as artifact.
        """

        self.validate_profile(obj)

        string_html = obj.to_html()

        string_json = obj.to_json()
        string_json = string_json.replace("NaN", "null")

        strio_html = write_bytesio(string_html)
        strio_json = write_bytesio(string_json)

        json_filename = self._fn_profile.format("pandas_profiling.json")
        html_filename = self._fn_profile.format("pandas_profiling.html")

        return [self.get_render_tuple(strio_html, html_filename),
                self.get_render_tuple(strio_json, json_filename)]
