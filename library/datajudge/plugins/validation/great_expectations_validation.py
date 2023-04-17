"""
GreatExpectations implementation of validation plugin.
"""
import os
from copy import deepcopy
from pathlib import Path
from typing import List

import great_expectations as ge
from great_expectations.core.expectation_validation_result import (
    ExpectationValidationResult,
)

from datajudge.metadata.datajudge_reports import DatajudgeReport
from datajudge.plugins.utils.great_expectations_utils import (
    get_great_expectations_validator,
)
from datajudge.plugins.utils.plugin_utils import exec_decorator
from datajudge.plugins.validation.validation_plugin import (
    Validation,
    ValidationPluginBuilder,
)
from datajudge.utils.commons import (
    LIBRARY_GREAT_EXPECTATIONS,
    PANDAS_DATAFRAME_FILE_READER,
)
from datajudge.utils.file_utils import clean_all


class ValidationPluginGreatExpectations(Validation):
    """
    GreatExpectations implementation of validation plugin.
    """

    def __init__(self) -> None:
        super().__init__()
        self.resource = None
        self.exec_multiprocess = True

    def setup(
        self,
        data_reader: "NativeReader",
        resource: "DataResource",
        constraint: "ConstraintGreatExpectations",
        error_report: str,
        exec_args: dict,
    ) -> None:
        """
        Set plugin resource.
        """

        self.data_reader = data_reader
        self.resource = resource
        self.constraint = constraint
        self.error_report = error_report
        self.exec_args = exec_args

    @exec_decorator
    def validate(self) -> dict:
        """
        Validate a Data Resource.
        """
        data = self.data_reader.fetch_data(self.resource.path)
        validator = get_great_expectations_validator(
            data, str(self.resource.name), str(self.resource.title)
        )
        validation_func = validator.validate_expectation(self.constraint.expectation)
        result = validation_func(**self.constraint.expectation_args)
        return ExpectationValidationResult(**result.to_json_dict())

    @exec_decorator
    def render_datajudge(self, result: "Result") -> DatajudgeReport:
        """
        Return a DatajudgeReport.
        """
        exec_err = result.errors
        duration = result.duration
        constraint = self.constraint.dict()
        errors = self._get_errors()

        if exec_err is None:
            res = deepcopy(result.artifact).to_json_dict()
            valid = res.get("success")
            observed = res.get("result", {})

            if not valid:
                if observed.get("observed_value") is not None:
                    total_count = 1
                    errors_list = [self._render_error_type("observed-value-error")]
                elif observed.get("unexpected_count") is not None:
                    total_count = observed.get("unexpected_count")
                    errors_list = [
                        self._render_error_type("unexpected-count-error")
                        for _ in range(total_count)
                    ]

                # AS debug if other type of errors are encountered
                else:
                    total_count = "Unknown"
                    errors_list = [self._render_error_type("unknown-error")]

                parsed_error_list = self._parse_error_report(errors_list)
                errors = self._get_errors(total_count, parsed_error_list)
        else:
            self.logger.error(f"Execution error {str(exec_err)} for plugin {self._id}")
            valid = False

        return DatajudgeReport(
            self.get_lib_name(),
            self.get_lib_version(),
            duration,
            constraint,
            valid,
            errors,
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
        filename = self._fn_report.format(f"{LIBRARY_GREAT_EXPECTATIONS}.json")
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


class ValidationBuilderGreatExpectations(ValidationPluginBuilder):
    """
    GreatExpectations validation plugin builder.
    """

    def build(
        self,
        resources: List["DataResource"],
        constraints: List["Constraint"],
        error_report: str,
    ) -> List[ValidationPluginGreatExpectations]:
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
                    data_reader = self._get_data_reader(
                        PANDAS_DATAFRAME_FILE_READER, store
                    )
                    plugin = ValidationPluginGreatExpectations()
                    plugin.setup(
                        data_reader, resource, const, error_report, self.exec_args
                    )
                    plugins.append(plugin)
        return plugins

    @staticmethod
    def _filter_constraints(
        constraints: List["Constraint"],
    ) -> List["ConstraintGreatExpectations"]:
        """
        Filter out ConstraintGreatExpectations.
        """
        return [
            const for const in constraints if const.type == LIBRARY_GREAT_EXPECTATIONS
        ]

    def destroy(self) -> None:
        """
        Destory plugins.
        """
        path = Path(os.getcwd(), "ge_ctxt")
        try:
            clean_all(path)
        except Exception:
            pass
