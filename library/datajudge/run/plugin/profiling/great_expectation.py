"""
GreatExpectation implementation of profiling plugin.
"""
# pylint: disable=import-error,no-name-in-module,arguments-differ,no-member,too-few-public-methods
from __future__ import annotations

import typing
from copy import deepcopy
from typing import List

import great_expectations as ge
from great_expectations.core.expectation_suite import ExpectationSuite
from great_expectations.profile.user_configurable_profiler import UserConfigurableProfiler

from datajudge.data import DatajudgeProfile
from datajudge.run.plugin.base_plugin import PluginBuilder
from datajudge.run.plugin.plugin_utils import exec_decorator
from datajudge.run.plugin.profiling.profiling_plugin import Profiling
from datajudge.utils.commons import GREAT_EXPECTATION
from datajudge.run.plugin.utils.dataframe_reader import DataFrameReader
from datajudge.run.plugin.utils.great_expectation_utils import get_great_expectation_validator

if typing.TYPE_CHECKING:
    from datajudge.data import DataResource
    from datajudge.run.plugin.base_plugin import Result


class ProfilePluginGreatExpectation(Profiling):
    """
    SQLAlchemy with GreatExpectation implementation of validation plugin.
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
    def profile(self) -> dict:
        """
        Profile a Data Resource.
        """
        data = DataFrameReader(self.resource.tmp_pth).read_df()
        validator = get_great_expectation_validator(data,
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
            fields = [i for i in res.get("meta", {}).get("columns", {}).keys()]
            stats = res.get("expectations")
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
        Return a rendered report ready to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = result.artifact.to_json_dict()
        filename = self._fn_report.format(f"{GREAT_EXPECTATION}.json")
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
            resource = self.fetch_resource(res)
            plugin = ProfilePluginGreatExpectation()
            plugin.setup(resource, self.exec_args)
            plugins.append(plugin)
        return plugins
