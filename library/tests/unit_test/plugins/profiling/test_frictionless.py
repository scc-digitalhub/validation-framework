import io

import frictionless
import pytest
from frictionless.resource import Resource

from datajudge.plugins.profiling.frictionless_profiling import (
    ProfileBuilderFrictionless,
    ProfilePluginFrictionless,
)
from datajudge.utils.commons import (
    LIBRARY_FRICTIONLESS,
    OPERATION_PROFILING,
    BASE_FILE_READER,
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


class TestProfilePluginFrictionless:
    @pytest.fixture(scope="class")
    def plugin(self):
        return ProfilePluginFrictionless

    @pytest.fixture(scope="class")
    def data_reader(self):
        return BASE_FILE_READER

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
        assert isinstance(output.artifact, Resource)

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
        filename = setted_plugin._fn_profile.format(f"{LIBRARY_FRICTIONLESS}.json")
        correct_render_artifact(output)
        assert isinstance(output.artifact[0].object, io.BytesIO)
        assert output.artifact[0].filename == filename

        # Error execution
        result = error_setted_plugin.profile()
        output = error_setted_plugin.render_artifact(result)
        incorrect_render_artifact(output)
        assert output.artifact[0].filename == filename

    def test_get_lib_name(self, plugin):
        assert plugin().get_lib_name() == frictionless.__name__

    def test_get_lib_version(self, plugin):
        assert plugin().get_lib_version() == frictionless.__version__


class TestProfileBuilderFrictionless:
    @pytest.fixture
    def plugin_builder(self, config_plugin_builder):
        return ProfileBuilderFrictionless(**config_plugin_builder)

    def test_build(self, plugin_builder):
        plugins = plugin_builder.build([RES_LOCAL_01])
        assert isinstance(plugins, list)
        assert len(plugins) == 1
        assert isinstance(plugins[0], ProfilePluginFrictionless)
