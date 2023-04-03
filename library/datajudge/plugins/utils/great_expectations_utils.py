"""
Great expectation utils module.
"""
import os
from pathlib import Path
from typing import Any

import pandas as pd
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.data_context.data_context import DataContext
from ruamel import yaml

from datajudge.utils.utils import get_uiid


def get_data_context() -> DataContext:
    """
    Create data context for great expectation.
    """
    base_path = Path(os.getcwd(), "ge_ctxt")
    tmp_path = Path(base_path, get_uiid())
    tmp_path.mkdir(parents=True)
    return DataContext.create(project_root_dir=tmp_path)


def get_great_expectations_validator(data: pd.DataFrame,
                                    data_source_name: str,
                                    data_asset_name: str) -> Any:
    """
    Get a great expectation validator to perfor validation
    or profiling.
    """

    expectation_suite_name = f"suite_{get_uiid()}"

    context = get_data_context()

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
        runtime_parameters={"batch_data": data},
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
    return validator
