# content of test_inference_plugin_frictionless.py

import frictionless
import pytest
from frictionless.schema import Schema

from datajudge.plugins.inference.frictionless_inference import (
    InferenceBuilderFrictionless,
    InferencePluginFrictionless,
)
from datajudge.utils.commons import (
    LIBRARY_FRICTIONLESS,
    OPERATION_INFERENCE,
    BASE_FILE_READER,
)
from tests.unit_test.plugins.utils_plugin_tests import (
    correct_execute,
    correct_setup,
    correct_render_artifact,
    correct_render_datajudge,
    incorrect_execute,
    incorrect_render_artifact,
    incorrect_render_datajudge,
)


class TestInferencePluginFrictionless:
    def test_setup(self, plugin):
        plg = plugin()
        plg.setup("test", "test", "test")
        correct_setup(plg)

    def test_infer(self, setted_plugin):
        # Correct execution
        output = setted_plugin.infer()
        correct_execute(output)
        assert isinstance(output.artifact, Schema)

        # Error execution
        setted_plugin.data_reader = "error"
        output = setted_plugin.infer()
        incorrect_execute(output)

    def test_render_datajudge(self, setted_plugin):
        # Correct execution
        result = setted_plugin.infer()
        output = setted_plugin.render_datajudge(result)
        correct_render_datajudge(output, OPERATION_INFERENCE)

        # Error execution
        setted_plugin.data_reader = "error"
        result = setted_plugin.infer()
        output = setted_plugin.render_datajudge(result)
        incorrect_render_datajudge(output, OPERATION_INFERENCE)

    def test_render_artifact_method(self, setted_plugin):
        # Correct execution
        result = setted_plugin.infer()
        output = setted_plugin.render_artifact(result)
        filename = setted_plugin._fn_schema.format(f"{LIBRARY_FRICTIONLESS}.json")
        correct_render_artifact(output)
        assert isinstance(output.artifact[0].object, dict)
        assert output.artifact[0].filename == filename

        # Error execution
        setted_plugin.data_reader = "error"
        result = setted_plugin.infer()
        output = setted_plugin.render_artifact(result)
        incorrect_render_artifact(output)
        assert output.artifact[0].filename == filename

    def test_get_lib_name(self, plugin):
        assert plugin().get_lib_name() == frictionless.__name__

    def test_get_lib_version(self, plugin):
        assert plugin().get_lib_version() == frictionless.__version__


class TestInferenceBuilderFrictionless:
    def test_build(self, plugin_builder, plugin_builder_non_val_args):
        plugins = plugin_builder.build(*plugin_builder_non_val_args)
        assert isinstance(plugins, list)
        assert len(plugins) == 1
        assert isinstance(plugins[0], InferencePluginFrictionless)


@pytest.fixture(scope="module")
def plugin():
    return InferencePluginFrictionless


@pytest.fixture
def plugin_builder(config_plugin_builder):
    return InferenceBuilderFrictionless(**config_plugin_builder)


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
    return BASE_FILE_READER
