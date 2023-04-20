import shutil
from pathlib import Path

import duckdb
import pytest

from datajudge.plugins.utils.plugin_utils import ValidationReport
from datajudge.plugins.validation.duckdb_validation import (
    ValidationBuilderDuckDB,
    ValidationPluginDuckDB,
)
from datajudge.utils.commons import (
    LIBRARY_DUCKDB,
    OPERATION_VALIDATION,
    PANDAS_DATAFRAME_DUCKDB_READER,
    DEFAULT_DIRECTORY,
)
from tests.conftest import CONST_DUCKDB_01
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


class TestValidationPluginDuckDB:
    def test_setup(self, plugin):
        plg = plugin()
        plg.setup("test", "test", "test", "test", "test")
        correct_setup(plg)

    def test_validate(self, setted_plugin):
        # Correct execution
        output = setted_plugin.validate()
        correct_execute(output)
        assert isinstance(output.artifact, ValidationReport)

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
        filename = setted_plugin._fn_report.format(f"{LIBRARY_DUCKDB}.json")
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
        assert plugin().get_lib_name() == duckdb.__name__

    def test_get_lib_version(self, plugin):
        assert plugin().get_lib_version() == duckdb.__version__


class TestValidationBuilderDuckDB:
    def test_build(self, plugin_builder, plugin_builder_val_args):
        plugins = plugin_builder.build(*plugin_builder_val_args)
        correct_plugin_build(plugins, ValidationPluginDuckDB)
        shutil.rmtree(Path(DEFAULT_DIRECTORY).parent)


@pytest.fixture
def plugin():
    return ValidationPluginDuckDB


@pytest.fixture
def plugin_builder(config_plugin_builder):
    return ValidationBuilderDuckDB(**config_plugin_builder)


@pytest.fixture
def config_plugin(reader, tmpduckdb, constraint, error_report):
    return [reader, tmpduckdb, constraint, error_report, {}]


@pytest.fixture
def store_cfg(local_store_cfg):
    return local_store_cfg


@pytest.fixture
def resource(local_resource):
    return local_resource


@pytest.fixture
def data_reader():
    return PANDAS_DATAFRAME_DUCKDB_READER


@pytest.fixture(params=[CONST_DUCKDB_01])
def constraint(request):
    return request.param
