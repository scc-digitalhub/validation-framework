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
from tests.conftest import RES_LOCAL_01
from tests.unit_test.plugins.utils_plugin_tests import (
    correct_execute,
    correct_render_artifact,
    correct_render_datajudge,
    incorrect_execute,
    incorrect_render_artifact,
    incorrect_render_datajudge,
)


class TestInferencePluginFrictionless:
    @pytest.fixture(scope="class")
    def plugin(self):
        return InferencePluginFrictionless

    @pytest.fixture(scope="class")
    def data_reader(self):
        return BASE_FILE_READER

    def test_setup(self, plugin):
        plg = plugin()
        plg.setup("test", "test", "test")
        assert plg.data_reader == "test"
        assert plg.resource == "test"
        assert plg.exec_args == "test"

    def test_infer(self, setted_plugin, error_setted_plugin):
        # Correct execution
        output = setted_plugin.infer()
        correct_execute(output)
        assert isinstance(output.artifact, Schema)

        # Error execution
        output = error_setted_plugin.infer()
        incorrect_execute(output)

    def test_render_datajudge(self, setted_plugin, error_setted_plugin):
        # Correct execution
        result = setted_plugin.infer()
        output = setted_plugin.render_datajudge(result)
        correct_render_datajudge(output, OPERATION_INFERENCE)

        # Error execution
        result = error_setted_plugin.infer()
        output = error_setted_plugin.render_datajudge(result)
        incorrect_render_datajudge(output, OPERATION_INFERENCE)

    def test_render_artifact_method(self, setted_plugin, error_setted_plugin):
        # Correct execution
        result = setted_plugin.infer()
        output = setted_plugin.render_artifact(result)
        filename = setted_plugin._fn_schema.format(f"{LIBRARY_FRICTIONLESS}.json")
        correct_render_artifact(output)
        assert isinstance(output.artifact[0].object, dict)
        assert output.artifact[0].filename == filename

        # Error execution
        result = error_setted_plugin.infer()
        output = error_setted_plugin.render_artifact(result)
        incorrect_render_artifact(output)
        assert output.artifact[0].filename == filename

    def test_get_lib_name(self, plugin):
        assert plugin().get_lib_name() == frictionless.__name__

    def test_get_lib_version(self, plugin):
        assert plugin().get_lib_version() == frictionless.__version__


class TestInferenceBuilderFrictionless:
    @pytest.fixture
    def plugin_builder(self, config_plugin_builder):
        return InferenceBuilderFrictionless(**config_plugin_builder)

    def test_build(self, plugin_builder):
        plugins = plugin_builder.build([RES_LOCAL_01])
        assert isinstance(plugins, list)
        assert len(plugins) == 1
        assert isinstance(plugins[0], InferencePluginFrictionless)
