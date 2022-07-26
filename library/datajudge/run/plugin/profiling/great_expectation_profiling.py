"""
GreatExpectation implementation of profiling plugin.
"""

from __future__ import annotations

import os
import typing
from copy import deepcopy
from pathlib import Path
from typing import List

import great_expectations as ge
from great_expectations.core.expectation_suite import ExpectationSuite
from great_expectations.profile.user_configurable_profiler import \
    UserConfigurableProfiler

from datajudge.data_reader.pandas_dataframe_reader import PandasDataFrameReader
from datajudge.metadata.datajudge_reports import DatajudgeProfile
from datajudge.run.plugin.base_plugin import PluginBuilder
from datajudge.run.plugin.profiling.profiling_plugin import Profiling
from datajudge.run.plugin.utils.great_expectation_utils import \
    get_great_expectation_validator
from datajudge.run.plugin.utils.plugin_utils import exec_decorator
from datajudge.utils.commons import LIBRARY_GREAT_EXPECTATION
from datajudge.utils.file_utils import clean_all

if typing.TYPE_CHECKING:
    from datajudge.data_reader.base_reader import DataReader
    from datajudge.metadata.data_resource import DataResource
    from datajudge.run.plugin.base_plugin import Result


class ProfilePluginGreatExpectation(Profiling):
    """
    SQLAlchemy with GreatExpectation implementation of validation plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.resource = None
        self.df = None
        self.exec_multiprocess = True

    def setup(self,
              data_reader: DataReader,
              resource: DataResource,
              exec_args: dict) -> None:
        """
        Set plugin resource.
        """
        self.resource = resource
        self.exec_args = exec_args
        self.df = data_reader.fetch_resource(self.resource.path)

    @exec_decorator
    def profile(self) -> dict:
        """
        Profile a Data Resource.
        """
        validator = get_great_expectation_validator(self.df,
                                                    str(self.resource.name),
                                                    str(self.resource.title))
        profiler = UserConfigurableProfiler(profile_dataset=validator)
        result = profiler.build_suite()
        return ExpectationSuite(**result.to_json_dict())

    @exec_decorator
    def render_datajudge(self, result: Result) -> DatajudgeProfile:
        """
        Return a DatajudgeProfile.
        """
        exec_err = result.errors
        duration = result.duration

        if exec_err is None:
            res = deepcopy(result.artifact).to_json_dict()
            fields = list(res.get("meta", {}).get("columns", {}).keys())
            stats = res.get("expectations")
        else:
            self.logger.error(
                f"Execution error {str(exec_err)} for plugin {self._id}")
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
        Return a rendered report ready to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = result.artifact.to_json_dict()
        filename = self._fn_profile.format(f"{LIBRARY_GREAT_EXPECTATION}.json")
        artifacts.append(self.get_render_tuple(_object, filename))
        return artifacts

    @staticmethod
    def get_lib_name() -> str:
        """
        Get library name.
        """
        return ge.__name__

    @staticmethod
    def get_lib_version() -> str:
        """
        Get library version.
        """
        return ge.__version__


class ProfileBuilderGreatExpectation(PluginBuilder):
    """
    Profile plugin builder.
    """

    def build(self,
              resources: List[DataResource]
              ) -> List[ProfilePluginGreatExpectation]:
        """
        Build a plugin.
        """
        plugins = []
        for res in resources:
            resource = self._get_resource_deepcopy(res)
            store = self._get_resource_store(resource)
            data_reader = PandasDataFrameReader(store, self.fetch_mode, self.reader_args)
            plugin = ProfilePluginGreatExpectation()
            plugin.setup(data_reader, resource, self.exec_args)
            plugins.append(plugin)
        return plugins

    def destroy(self) -> None:
        """
        Destory plugins.
        """
        path = Path(os.getcwd(), "ge_ctxt")
        clean_all(path)
