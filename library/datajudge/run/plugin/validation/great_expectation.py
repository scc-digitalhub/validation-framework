"""
GreatExpectation implementation of validation plugin.
"""

from __future__ import annotations

import os
import typing
from copy import deepcopy
from pathlib import Path
from typing import List

import great_expectations as ge
from great_expectations.core.expectation_validation_result import \
    ExpectationValidationResult

from datajudge.data_reader.pandas_dataframe_reader import PandasDataFrameReader
from datajudge.metadata import DatajudgeReport
from datajudge.run.plugin.utils.great_expectation_utils import \
    get_great_expectation_validator
from datajudge.run.plugin.utils.plugin_utils import exec_decorator
from datajudge.run.plugin.validation.validation_plugin import (
    Validation, ValidationPluginBuilder)
from datajudge.utils.commons import LIBRARY_GREAT_EXPECTATION
from datajudge.utils.file_utils import clean_all
from datajudge.utils.utils import listify

if typing.TYPE_CHECKING:
    from datajudge.data_reader.base_reader import DataReader
    from datajudge.metadata import DataResource
    from datajudge.run.plugin.base_plugin import Result
    from datajudge.utils.config import Constraint, ConstraintGreatExpectation


class ValidationPluginGreatExpectation(Validation):
    """
    GreatExpectation implementation of validation plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.constraint = None
        self.resource = None
        self.exec_args = None
        self.exec_multiprocess = True

    def setup(self,
              data_reader: DataReader,
              resource: DataResource,
              constraint: ConstraintGreatExpectation,
              exec_args: dict) -> None:
        """
        Set plugin resource.
        """
        self.resource = resource
        self.constraint = constraint
        self.exec_args = exec_args
        self.df = data_reader.fetch_resource(self.resource.path)

    @exec_decorator
    def validate(self) -> dict:
        """
        Validate a Data Resource.
        """
        validator = get_great_expectation_validator(self.df,
                                                    str(self.resource.name),
                                                    str(self.resource.title))
        validation_func = validator.validate_expectation(
            self.constraint.expectation)
        result = validation_func(**self.constraint.expectation_args)
        return ExpectationValidationResult(**result.to_json_dict())

    @exec_decorator
    def render_datajudge(self, result: Result) -> DatajudgeReport:
        """
        Return a DatajudgeReport.
        """
        exec_err = result.errors
        duration = result.duration
        constraint = self.constraint.dict()

        if exec_err is None:
            res = deepcopy(result.artifact).to_json_dict()
            valid = res.get("success")
            if not valid:
                errors = listify(res.get("result"))
            else:
                errors = None
        else:
            self.logger.error(
                f"Execution error {str(exec_err)} for plugin {self._id}")
            valid = False
            errors = None

        return DatajudgeReport(self.get_lib_name(),
                               self.get_lib_version(),
                               duration,
                               constraint,
                               valid,
                               errors)

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
        filename = self._fn_report.format(f"{LIBRARY_GREAT_EXPECTATION}.json")
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


class ValidationBuilderGreatExpectation(ValidationPluginBuilder):
    """
    GreatExpectation validation plugin builder.
    """

    def build(self,
              resources: List[DataResource],
              constraints: List[Constraint]
              ) -> List[ValidationPluginGreatExpectation]:
        """
        Build a plugin for every resource and every constraint.
        """
        f_constraints = self._filter_constraints(constraints)
        plugins = []
        for res in resources:
            resource = self._get_resource_deepcopy(res)
            for const in f_constraints:
                if resource.name in const.resources:
                    store = self._get_resource_store(resource)
                    data_reader = PandasDataFrameReader(store, self.fetch_mode, self.reader_args)
                    plugin = ValidationPluginGreatExpectation()
                    plugin.setup(data_reader, resource, const, self.exec_args)
                    plugins.append(plugin)
        return plugins

    @staticmethod
    def _filter_constraints(constraints: List[Constraint]
                            ) -> List[ConstraintGreatExpectation]:
        """
        Filter out ConstraintGreatExpectation.
        """
        return [const for const in constraints if const.type == LIBRARY_GREAT_EXPECTATION]

    def destroy(self) -> None:
        """
        Destory plugins.
        """
        path = Path(os.getcwd(), "ge_ctxt")
        clean_all(path)
