import io

import frictionless
import pytest
from frictionless.resource import Resource

from datajudge.plugins.profiling.frictionless_profiling import (
    ProfileBuilderFrictionless,
    ProfilePluginFrictionless,
)
from datajudge.utils.commons import (
    BASE_FILE_READER,
    LIBRARY_FRICTIONLESS,
    OPERATION_PROFILING,
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


class TestProfilePluginFrictionless:
    def test_setup(self, plugin):
        plg = plugin()
        plg.setup("test", "test", "test")
        correct_setup(plg)

    def test_profile(self, setted_plugin):
        # Correct execution
        output = setted_plugin.profile()
        correct_execute(output)
        assert isinstance(output.artifact, Resource)

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
        filename = setted_plugin._fn_profile.format(f"{LIBRARY_FRICTIONLESS}.json")
        correct_render_artifact(output)
        assert isinstance(output.artifact[0].object, io.BytesIO)
        assert output.artifact[0].filename == filename

        # Error execution
        setted_plugin.data_reader = "error"
        result = setted_plugin.profile()
        output = setted_plugin.render_artifact(result)
        incorrect_render_artifact(output)
        assert output.artifact[0].filename == filename

    def test_get_lib_name(self, plugin):
        assert plugin().get_lib_name() == frictionless.__name__

    def test_get_lib_version(self, plugin):
        assert plugin().get_lib_version() == frictionless.__version__


class TestProfileBuilderFrictionless:
    def test_build(self, plugin_builder, plugin_builder_non_val_args):
        plugins = plugin_builder.build(*plugin_builder_non_val_args)
        correct_plugin_build(plugins, ProfilePluginFrictionless)


@pytest.fixture
def plugin():
    return ProfilePluginFrictionless


@pytest.fixture
def plugin_builder(config_plugin_builder):
    return ProfileBuilderFrictionless(**config_plugin_builder)


@pytest.fixture
def config_plugin(reader, resource):
    return [reader, resource, {}]


@pytest.fixture
def store_cfg(local_store_cfg):
    return local_store_cfg


@pytest.fixture
def resource(local_resource):
    return local_resource


@pytest.fixture
def data_reader():
    return BASE_FILE_READER
