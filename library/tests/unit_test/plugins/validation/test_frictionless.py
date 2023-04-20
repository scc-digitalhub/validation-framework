from copy import deepcopy

import frictionless
import pytest
from frictionless.exception import FrictionlessException
from frictionless.report import Report
from frictionless.schema import Schema

from datajudge.plugins.validation.frictionless_validation import (
    ValidationBuilderFrictionless,
    ValidationPluginFrictionless,
)
from datajudge.utils.commons import (
    LIBRARY_FRICTIONLESS,
    CONSTRAINT_FRICTIONLESS_SCHEMA,
    OPERATION_VALIDATION,
    BASE_FILE_READER,
)
from tests.conftest import (
    CONST_FRICT_01,
    CONST_FRICT_FULL_01,
)
from tests.unit_test.plugins.utils_plugin_tests import (
    correct_execute,
    correct_plugin_build,
    correct_setup,
    correct_render_artifact,
    correct_render_datajudge,
    incorrect_execute,
    incorrect_render_artifact,
    incorrect_render_datajudge,
)


class TestValidationPluginFrictionless:
    def test_setup(self, plugin):
        plg = plugin()
        plg.setup("test", "test", "test", "test", "test")
        correct_setup(plg)

    def test_validate(self, setted_plugin):
        # Correct execution
        output = setted_plugin.validate()
        correct_execute(output)
        assert isinstance(output.artifact, Report)

        # Error execution
        setted_plugin.data_reader = "error"
        output = setted_plugin.validate()
        incorrect_execute(output)

    def test_render_datajudge(self, setted_plugin):
        # Correct execution
        result = setted_plugin.validate()
        output = setted_plugin.render_datajudge(result)
        correct_render_datajudge(output, OPERATION_VALIDATION)

        # Error execution
        setted_plugin.data_reader = "error"
        result = setted_plugin.validate()
        output = setted_plugin.render_datajudge(result)
        incorrect_render_datajudge(output, OPERATION_VALIDATION)

    def test_render_artifact_method(self, setted_plugin):
        # Correct execution
        result = setted_plugin.validate()
        output = setted_plugin.render_artifact(result)
        filename = setted_plugin._fn_report.format(f"{LIBRARY_FRICTIONLESS}.json")
        correct_render_artifact(output)
        assert isinstance(output.artifact[0].object, dict)
        assert output.artifact[0].filename == filename

        # Error execution
        setted_plugin.data_reader = "error"
        result = setted_plugin.validate()
        output = setted_plugin.render_artifact(result)
        incorrect_render_artifact(output)
        assert output.artifact[0].filename == filename

    def test_get_lib_name(self, plugin):
        assert plugin().get_lib_name() == frictionless.__name__

    def test_get_lib_version(self, plugin):
        assert plugin().get_lib_version() == frictionless.__version__

    def test_rebuild_constraints(self, setted_plugin):
        # Correct execution
        path = setted_plugin.data_reader.fetch_data(setted_plugin.resource.path)
        schema = setted_plugin._rebuild_constraints(path)
        assert isinstance(schema, Schema)

        # Error execution (malformed table schema)
        if setted_plugin.constraint.type == CONSTRAINT_FRICTIONLESS_SCHEMA:
            with pytest.raises(FrictionlessException):
                # Deepcopy plugin, otherwise setting constraint
                # influence subsequent tests
                plg = deepcopy(setted_plugin)
                plg.constraint.tableSchema = "error"
                plg._rebuild_constraints(None)

    def test_get_schema(self, plugin, data_path_csv, data_path_parquet):
        assert isinstance(plugin._get_schema(data_path_csv), dict)
        assert plugin._get_schema(data_path_parquet) == {"fields": []}
        with pytest.raises(FrictionlessException):
            plugin._get_schema("error")

class TestValidationBuilderFrictionless:
    def test_build(self, plugin_builder, plugin_builder_val_args):
        plugins = plugin_builder.build(*plugin_builder_val_args)
        correct_plugin_build(plugins, ValidationPluginFrictionless)


@pytest.fixture
def plugin():
    return ValidationPluginFrictionless


@pytest.fixture
def plugin_builder(config_plugin_builder):
    return ValidationBuilderFrictionless(**config_plugin_builder)


@pytest.fixture
def config_plugin(reader, constraint, resource, error_report):
    return [reader, resource, constraint, error_report, {}]


@pytest.fixture
def store_cfg(local_store_cfg):
    return local_store_cfg


@pytest.fixture
def resource(local_resource):
    return local_resource


@pytest.fixture
def data_reader():
    return BASE_FILE_READER


@pytest.fixture(params=[CONST_FRICT_01, CONST_FRICT_FULL_01])
def constraint(request):
    return request.param
