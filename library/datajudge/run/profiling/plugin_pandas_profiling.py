"""
RunInference class module.
The RunInference class describes a Run object that performs
inference tasks over a Resource. With inference task, we mean
a general description of a resource (extension, metadata etc.)
and the inference of a data schema (field types).
"""
# pylint: disable=import-error,invalid-name
from __future__ import annotations

import json
import typing
from typing import List, Optional, Tuple, Union

import pandas as pd
try:
    import pandas_profiling
    from pandas_profiling import ProfileReport
except ImportError as ierr:
    raise ImportError("Please install pandas_profiling!") from ierr

from datajudge.data.short_profile import ProfileTuple
from datajudge.run.profiling.profiling_plugin import Profiling
from datajudge.utils.utils import time_to_sec

if typing.TYPE_CHECKING:
    from datajudge.data import DataResource


# COLUMNS/FIELDS TO PARSE FROM PROFILE
PROFILE_COLUMNS = ["analysis", "table", "variables"]
PROFILE_FIELDS = ["n_distinct", "p_distinct", "is_unique",
                  "n_unique", "p_unique", "type", "hashable",
                  "n_missing", "n", "p_missing", "count",
                  "memory_size"]


class InferencePluginPandasProfiling(Profiling):

    def update_library_info(self) -> None:
        """
        Update run's info about the validation framework used.
        """
        self.lib_name = pandas_profiling.__name__
        self.lib_version = pandas_profiling.__version__
   
    def parse_profile(self,
                      profile: ProfileReport) -> ProfileTuple:
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
        var = args.get("variables")
        for key in var:
            args["variables"][key] = {
                k: var[key][k] for k in PROFILE_FIELDS
            }

        # "Rename" variables with fields and tables with stats
        args["fields"] = args.pop("variables")
        args["stats"] = args.pop("table")

        # Extract duration from analysis and set as key
        # and pop analysis
        duration = args.get("analysis", {}).get("duration")
        args["duration"] = time_to_sec(duration)
        args.pop("analysis")

        tup = ProfileTuple(
            args["duration"],
            args["stats"],
            args["fields"]
        )

        return tup

    def validate_profile(self,
                         profile: Optional[ProfileReport] = None
                        ) -> None:
        """
        Validate the profile.
        """
        if profile is not None and not isinstance(profile, ProfileReport):
            raise TypeError("Expected pandas_profiling Profile!")

    def profile(self,
                data_path: str,
                profiler_kwargs: dict = None,
                resource: DataResource = None) -> ProfileReport:
        """
        Generate pandas_profiling profile.

        Parameters
        ----------
        **kwargs : dict
            Parameters for pandas_profiling.ProfileReport.

        """
        if profiler_kwargs is None:
            profiler_kwargs = {}
       
        file_format, pandas_kwargs = self._parse_resource(resource)
        df = self._read_df(data_path,
                           file_format,
                           **pandas_kwargs)
        profile = ProfileReport(df, **profiler_kwargs)
        return profile
   
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

    def _parse_resource(self,
                        resource: DataResource = None
                        ) -> Tuple[str, dict]:
        """
        Parse DataResource and return file format and
        optional arguments for pandas.
        """

        pandas_args = {}

        file_format = getattr(resource, "format")
        if file_format is None:
            file_format = "csv"
        pandas_args["sep"] = ","
        pandas_args["encoding"] = "utf-8"

        # Redo this part
        # Default args for read_csv: sep ",", encoding "utf-8"
        # if file_format == "csv":
        #     pandas_args["sep"] = self.inferred.get("dialect", {})\
        #                                       .get("delimiter", ",")
        #     pandas_args["encoding"] = self.inferred.get("encoding", "utf-8")

        return file_format, pandas_args
