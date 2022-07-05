"""
GreatExpectation implementation of validation plugin.
"""
# pylint: disable=import-error,no-name-in-module,arguments-differ,no-member,too-few-public-methods
from __future__ import annotations

import typing
from copy import deepcopy
from typing import List

import great_expectations as ge
import pandas as pd
from great_expectations.core.batch import RuntimeBatchRequest
from ruamel import yaml

from datajudge.data import DatajudgeReport
from datajudge.run.plugin.plugin_utils import exec_decorator
from datajudge.run.plugin.validation.validation_plugin import (
    Validation, ValidationPluginBuilder)
from datajudge.utils.commons import GREAT_EXPECTATION
from datajudge.utils.dataframe_reader import DataFrameReader
from datajudge.utils.utils import get_uiid, listify

if typing.TYPE_CHECKING:
    from datajudge.data import DataResource
    from datajudge.run.plugin.base_plugin import Result
    from datajudge.utils.config import Constraint, ConstraintsGreatExpectation


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
              resource: DataResource,
              constraint: ConstraintsGreatExpectation,
              exec_args: dict) -> None:
        """
        Set plugin resource.
        """
        self.resource = resource
        self.constraint = constraint
        self.exec_args = exec_args

    @exec_decorator
    def validate(self) -> dict:
        """
        Validate a Data Resource.
        """
        data = DataFrameReader(self.resource.tmp_pth).read_df()
        report = self.evaluate_validity_ge(data,
                                           self.constraint.expectation,
                                           self.constraint.expectation_args)
        return report

    def evaluate_validity_ge(self,
                             df: pd.DataFrame,
                             func_name: str,
                             func_args: dict) -> dict:

        context = ge.get_context()
        data_source_name = str(self.resource.name)
        data_asset_name = str(self.resource.title)
        expectation_suite_name = f"suite_{get_uiid()}"

        datasource_config = {
            "name": data_source_name,
            "class_name": "Datasource",
            "module_name": "great_expectations.datasource",
            "execution_engine": {
                "module_name": "great_expectations.execution_engine",
                "class_name": "PandasExecutionEngine",
            },
            "data_connectors": {
                "default_runtime_data_connector_name": {
                    "class_name": "RuntimeDataConnector",
                    "module_name": "great_expectations.datasource.data_connector",
                    "batch_identifiers": ["default_identifier_name"],
                },
            },
        }

        context.test_yaml_config(yaml.dump(datasource_config))
        context.add_datasource(**datasource_config)

        batch_request = RuntimeBatchRequest(
            datasource_name=data_source_name,
            data_connector_name="default_runtime_data_connector_name",
            data_asset_name=data_asset_name,
            runtime_parameters={"batch_data": df},
            batch_identifiers={"default_identifier_name": "default_identifier"},
        )
        context.create_expectation_suite(
            expectation_suite_name=expectation_suite_name,
            overwrite_existing=True
        )
        validator = context.get_validator(
            batch_request=batch_request,
            expectation_suite_name=expectation_suite_name
        )

        validation_func = validator.validate_expectation(func_name)
        results = validation_func(**func_args)
        return results

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
            errors = listify(res.get("result"))
        else:
            self.logger.error(f"Execution error {str(exec_err)} for plugin {self._id}")
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
        f_constraints = self.filter_constraints(constraints)
        plugins = []
        for res in resources:
            resource = self.fetch_resource(res)
            for const in f_constraints:
                if resource.name in const.resources:
                    plugin = ValidationPluginGreatExpectation()
                    plugin.setup(resource, const, self.exec_args)
                    plugins.append(plugin)
        return plugins

    @staticmethod
    def filter_constraints(constraints: List[Constraint]
                           ) -> List[ConstraintsGreatExpectation]:
        return [const for const in constraints if const.type==GREAT_EXPECTATION]

    def destroy(self) -> None:
        """
        Destory plugins.
        """
