from typing import Any

import great_expectations as ge
import pandas as pd
from great_expectations.core.batch import RuntimeBatchRequest
from ruamel import yaml

from datajudge.utils.utils import get_uiid


def get_great_expectation_validator(data: pd.DataFrame,
                                    data_source_name: str,
                                    data_asset_name: str) -> Any:
    #great_expectations init

    expectation_suite_name = f"suite_{get_uiid()}"

    context = ge.get_context()

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
