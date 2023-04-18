"""
GreatExpectations implementation of profiling plugin.
"""
import os
from copy import deepcopy
from pathlib import Path
from typing import List

import great_expectations as ge
from great_expectations.core.expectation_suite import ExpectationSuite
from great_expectations.profile.user_configurable_profiler import (
    UserConfigurableProfiler,
)

from datajudge.metadata.datajudge_reports import DatajudgeProfile
from datajudge.plugins.base_plugin import PluginBuilder
from datajudge.plugins.profiling.profiling_plugin import Profiling
from datajudge.plugins.utils.great_expectations_utils import (
    get_great_expectations_validator,
)
from datajudge.plugins.utils.plugin_utils import exec_decorator
from datajudge.utils.commons import (
    LIBRARY_GREAT_EXPECTATIONS,
    PANDAS_DATAFRAME_FILE_READER,
)
from datajudge.utils.file_utils import clean_all


class ProfilePluginGreatExpectations(Profiling):
    """
    SQLAlchemy with GreatExpectations implementation of validation plugin.
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
    def profile(self) -> dict:
        """
        Profile a Data Resource.
        """
        data = self.data_reader.fetch_data(self.resource.path)
        validator = get_great_expectations_validator(
            data, str(self.resource.name), str(self.resource.title)
        )
        profiler = UserConfigurableProfiler(profile_dataset=validator)
        result = profiler.build_suite()
        return ExpectationSuite(**result.to_json_dict())

    @exec_decorator
    def render_datajudge(self, result: "Result") -> DatajudgeProfile:
        """
        Return a DatajudgeProfile.
        """
        exec_err = result.errors
        duration = result.duration

        if exec_err is None:
            res = deepcopy(result.artifact).to_json_dict()
            fields = {"fields": list(res.get("meta", {}).get("columns", {}).keys())}
            stats = {"stats": list(res.get("expectations"))}
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
        Return a rendered report ready to be persisted as artifact.
        """
        artifacts = []
        if result.artifact is None:
            _object = {"errors": result.errors}
        else:
            _object = result.artifact.to_json_dict()
        filename = self._fn_profile.format(f"{LIBRARY_GREAT_EXPECTATIONS}.json")
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


class ProfileBuilderGreatExpectations(PluginBuilder):
    """
    Profile plugin builder.
    """

    def build(
        self, resources: List["DataResource"]
    ) -> List[ProfilePluginGreatExpectations]:
        """
        Build a plugin.
        """
        plugins = []
        for res in resources:
            resource = self._get_resource_deepcopy(res)
            store = self._get_resource_store(resource)
            data_reader = self._get_data_reader(PANDAS_DATAFRAME_FILE_READER, store)
            plugin = ProfilePluginGreatExpectations()
            plugin.setup(data_reader, resource, self.exec_args)
            plugins.append(plugin)
        return plugins

    def destroy(self) -> None:
        ...
