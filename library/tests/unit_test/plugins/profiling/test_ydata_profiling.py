import io

import ydata_profiling
import pytest
from ydata_profiling import ProfileReport

from datajudge.plugins.profiling.ydata_profiling_profiling import (
    ProfileBuilderYdataProfiling,
    ProfilePluginYdataProfiling,
)
from datajudge.utils.commons import (
    LIBRARY_YDATA_PROFILING,
    OPERATION_PROFILING,
    PANDAS_DATAFRAME_FILE_READER,
)
from tests.conftest import RES_LOCAL_01
from tests.unit_test.plugins.utils_plugin_tests import (
    correct_execute,
    correct_render_artifact,
    correct_render_datajudge,
    incorrect_execute,
    incorrect_render_artifact,
    incorrect_render_datajudge,
)


class TestProfilePluginYdataProfiling:
    @pytest.fixture(scope="class")
    def plugin(self):
        return ProfilePluginYdataProfiling

    @pytest.fixture(scope="class")
    def data_reader(self):
        return PANDAS_DATAFRAME_FILE_READER

    def test_setup(self, plugin):
        plg = plugin()
        plg.setup("test", "test", "test")
        assert plg.data_reader == "test"
        assert plg.resource == "test"
        assert plg.exec_args == "test"

    def test_profile(self, setted_plugin, error_setted_plugin):
        # Correct execution
        output = setted_plugin.profile()
        correct_execute(output)
        assert isinstance(output.artifact, ProfileReport)

        # Error execution
        output = error_setted_plugin.profile()
        incorrect_execute(output)

    def test_render_datajudge(self, setted_plugin, error_setted_plugin):
        # Correct execution
        result = setted_plugin.profile()
        output = setted_plugin.render_datajudge(result)
        correct_render_datajudge(output, OPERATION_PROFILING)

        # Error execution
        result = error_setted_plugin.profile()
        output = error_setted_plugin.render_datajudge(result)
        incorrect_render_datajudge(output, OPERATION_PROFILING)

    def test_render_artifact_method(self, setted_plugin, error_setted_plugin):
        # Correct execution
        result = setted_plugin.profile()
        output = setted_plugin.render_artifact(result)
        filename1 = setted_plugin._fn_profile.format(f"{LIBRARY_YDATA_PROFILING}.json")
        filename2 = setted_plugin._fn_profile.format(f"{LIBRARY_YDATA_PROFILING}.html")
        correct_render_artifact(output)
        assert isinstance(output.artifact[0].object, io.BytesIO)
        assert output.artifact[0].filename == filename2
        assert isinstance(output.artifact[1].object, io.BytesIO)
        assert output.artifact[1].filename == filename1

        # Error execution
        result = error_setted_plugin.profile()
        output = error_setted_plugin.render_artifact(result)
        incorrect_render_artifact(output)
        assert output.artifact[0].filename == filename1
        assert output.artifact[0].filename != filename2

    def test_get_lib_name(self, plugin):
        assert plugin().get_lib_name() == ydata_profiling.__name__

    def test_get_lib_version(self, plugin):
        assert plugin().get_lib_version() == ydata_profiling.__version__


class TestProfileBuilderYdataProfiling:
    @pytest.fixture
    def plugin_builder(self, config_plugin_builder):
        return ProfileBuilderYdataProfiling(**config_plugin_builder)

    def test_build(self, plugin_builder):
        plugins = plugin_builder.build([RES_LOCAL_01])
        assert isinstance(plugins, list)
        assert len(plugins) == 1
        assert isinstance(plugins[0], ProfilePluginYdataProfiling)
