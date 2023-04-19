import pytest
import sqlalchemy

from datajudge.plugins.utils.plugin_utils import ValidationReport
from datajudge.plugins.validation.sqlalchemy_validation import (
    ValidationBuilderSqlAlchemy,
    ValidationPluginSqlAlchemy,
)
from datajudge.utils.commons import (
    LIBRARY_SQLALCHEMY,
    OPERATION_VALIDATION,
    PANDAS_DATAFRAME_SQL_READER,
)
from tests.conftest import CONST_SQLALCHEMY_01
from tests.unit_test.plugins.utils_plugin_tests import (
    correct_execute,
    correct_setup,
    correct_render_artifact,
    correct_render_datajudge,
    incorrect_execute,
    incorrect_render_artifact,
    incorrect_render_datajudge,
)


class TestValidationPluginSqlAlchemy:
    def test_setup(self, plugin):
        plg = plugin()
        plg.setup("test", "test", "test", "test")
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
        filename = setted_plugin._fn_report.format(f"{LIBRARY_SQLALCHEMY}.json")
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
        assert plugin().get_lib_name() == sqlalchemy.__name__

    def test_get_lib_version(self, plugin):
        assert plugin().get_lib_version() == sqlalchemy.__version__


class TestValidationBuilderSqlAlchemy:
    def test_build(self, plugin_builder, plugin_builder_val_args):
        plugins = plugin_builder.build(*plugin_builder_val_args)
        assert isinstance(plugins, list)
        assert len(plugins) == 1
        assert isinstance(plugins[0], ValidationPluginSqlAlchemy)


@pytest.fixture(scope="module")
def plugin():
    return ValidationPluginSqlAlchemy


@pytest.fixture
def plugin_builder(config_plugin_builder):
    return ValidationBuilderSqlAlchemy(**config_plugin_builder)


@pytest.fixture
def config_plugin(reader, constraint, error_report):
    return [reader, constraint, error_report, {}]


@pytest.fixture
def store_cfg(sql_store_cfg):
    return sql_store_cfg


@pytest.fixture
def resource(sql_resource):
    return sql_resource


@pytest.fixture(scope="module")
def data_reader():
    return PANDAS_DATAFRAME_SQL_READER


@pytest.fixture(scope="module", params=[CONST_SQLALCHEMY_01])
def constraint(request):
    return request.param
