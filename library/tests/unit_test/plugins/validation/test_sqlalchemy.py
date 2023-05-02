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
    correct_plugin_build,
    correct_setup,
    correct_render_artifact,
    correct_render_datajudge,
    incorrect_execute,
    incorrect_render_artifact,
    incorrect_render_datajudge,
    mock_c_sqlalc,
    mock_c_generic,
    mock_s_generic,
    mock_r_generic,
    mock_c_to_fail,
    mock_s_to_fail,
    mock_r_to_fail,
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
        correct_plugin_build(plugins, ValidationPluginSqlAlchemy)

    # fmt: off
    @pytest.mark.parametrize(
        "const_list,len_list",
        [
            ([mock_c_sqlalc, mock_c_sqlalc,], 2),
            ([mock_c_sqlalc, mock_c_generic,], 1),
            ([mock_c_generic,], 0),
            ([mock_c_generic, mock_c_generic,], 0),
        ]
    )
    # fmt: on
    def test_filter_constraints(self, plugin_builder, const_list, len_list):
        assert len(plugin_builder._filter_constraints(const_list)) == len_list

    # fmt: off
    @pytest.mark.parametrize(
        "store_list,const_list,res_list,len_list",
        [
            ([mock_s_generic], [mock_c_generic], [mock_r_generic], 1),
            ([mock_s_to_fail], [mock_c_generic], [mock_r_generic], 0),
            ([mock_s_generic], [mock_c_to_fail], [mock_r_generic], 0),
            # This gives 2 because the resource filtering happens before
            ([mock_s_generic], [mock_c_generic], [mock_r_generic, mock_r_generic], 2),
            ([mock_s_generic, mock_s_to_fail], [mock_c_generic, mock_c_to_fail], [mock_r_generic, mock_r_to_fail], 2),
        ],
    )
    # fmt: on
    def test_filter_resources(
        self, plugin_builder, store_list, const_list, res_list, len_list
    ):
        plugin_builder.stores = store_list
        assert len(plugin_builder._filter_resources(res_list, const_list)) == len_list

    def test_regroup_constraint_resources(self, plugin_builder):
        plugin_builder.stores = [mock_s_generic]
        regroup = plugin_builder._regroup_constraint_resources(
            [mock_c_generic], [mock_r_generic]
        )
        assert regroup == [{"constraint": mock_c_generic, "store": mock_s_generic,},]


@pytest.fixture
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


@pytest.fixture
def data_reader():
    return PANDAS_DATAFRAME_SQL_READER


@pytest.fixture(params=[CONST_SQLALCHEMY_01])
def constraint(request):
    return request.param
