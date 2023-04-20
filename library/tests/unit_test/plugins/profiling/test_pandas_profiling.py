import io

import pandas_profiling
import pytest
from pandas_profiling import ProfileReport

from datajudge.plugins.profiling.pandas_profiling_profiling import (
    ProfileBuilderPandasProfiling,
    ProfilePluginPandasProfiling,
)
from datajudge.utils.commons import (
    LIBRARY_PANDAS_PROFILING,
    OPERATION_PROFILING,
    PANDAS_DATAFRAME_FILE_READER,
)
from tests.unit_test.plugins.utils_plugin_tests import (
    correct_execute,
    correct_plugin_build,
    correct_render_artifact,
    correct_render_datajudge,
    incorrect_execute,
    incorrect_render_artifact,
    incorrect_render_datajudge,
    correct_setup,
)


class TestProfilePluginPandasProfiling:
    def test_setup(self, plugin):
        plg = plugin()
        plg.setup("test", "test", "test")
        correct_setup(plg)

    def test_profile(self, setted_plugin):
        # Correct execution
        output = setted_plugin.profile()
        correct_execute(output)
        assert isinstance(output.artifact, ProfileReport)

        # Error execution
        setted_plugin.data_reader = "error"
        output = setted_plugin.profile()
        incorrect_execute(output)

    def test_render_datajudge(self, setted_plugin):
        # Correct execution
        result = setted_plugin.profile()
        output = setted_plugin.render_datajudge(result)
        correct_render_datajudge(output, OPERATION_PROFILING)

        # Error execution
        setted_plugin.data_reader = "error"
        result = setted_plugin.profile()
        output = setted_plugin.render_datajudge(result)
        incorrect_render_datajudge(output, OPERATION_PROFILING)

    def test_render_artifact_method(self, setted_plugin):
        # Correct execution
        result = setted_plugin.profile()
        output = setted_plugin.render_artifact(result)
        filename1 = setted_plugin._fn_profile.format(f"{LIBRARY_PANDAS_PROFILING}.json")
        filename2 = setted_plugin._fn_profile.format(f"{LIBRARY_PANDAS_PROFILING}.html")
        correct_render_artifact(output)
        assert isinstance(output.artifact[0].object, io.BytesIO)
        assert output.artifact[0].filename == filename2
        assert isinstance(output.artifact[1].object, io.BytesIO)
        assert output.artifact[1].filename == filename1

        # Error execution
        setted_plugin.data_reader = "error"
        result = setted_plugin.profile()
        output = setted_plugin.render_artifact(result)
        incorrect_render_artifact(output)
        assert output.artifact[0].filename == filename1
        assert output.artifact[0].filename != filename2

    def test_get_lib_name(self, plugin):
        assert plugin().get_lib_name() == pandas_profiling.__name__

    def test_get_lib_version(self, plugin):
        assert plugin().get_lib_version() == pandas_profiling.__version__


class TestProfileBuilderPandasProfiling:
    def test_build(self, plugin_builder, plugin_builder_non_val_args):
        plugins = plugin_builder.build(*plugin_builder_non_val_args)
        correct_plugin_build(plugins, ProfilePluginPandasProfiling)


@pytest.fixture(scope="module")
def plugin():
    return ProfilePluginPandasProfiling


@pytest.fixture
def plugin_builder(config_plugin_builder):
    return ProfileBuilderPandasProfiling(**config_plugin_builder)


@pytest.fixture
def config_plugin(reader, resource):
    return [reader, resource, {}]


@pytest.fixture
def store_cfg(local_store_cfg):
    return local_store_cfg


@pytest.fixture
def resource(local_resource):
    return local_resource


@pytest.fixture(scope="module")
def data_reader():
    return PANDAS_DATAFRAME_FILE_READER
