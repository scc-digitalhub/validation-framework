import pytest

from datajudge.plugins.inference.dummy_inference import (
    InferenceBuilderDummy,
    InferencePluginDummy,
)
from datajudge.utils.commons import LIBRARY_DUMMY, OPERATION_INFERENCE, BASE_FILE_READER
from tests.conftest import RES_LOCAL_01
from tests.unit_test.plugins.utils_plugin_tests import (
    correct_execute,
    correct_render_artifact,
    correct_render_datajudge,
)


class TestInferencePluginDummy:
    @pytest.fixture(scope="class")
    def plugin(self):
        return InferencePluginDummy

    @pytest.fixture(scope="class")
    def data_reader(self):
        return BASE_FILE_READER

    def test_infer(self, setted_plugin):
        output = setted_plugin.infer()
        correct_execute(output)
        assert isinstance(output.artifact, dict)

    def test_render_datajudge(self, setted_plugin):
        result = setted_plugin.infer()
        output = setted_plugin.render_datajudge(result)
        correct_render_datajudge(output, OPERATION_INFERENCE)

    def test_render_artifact_method(self, setted_plugin):
        result = setted_plugin.infer()
        output = setted_plugin.render_artifact(result)
        filename = setted_plugin._fn_schema.format(f"{LIBRARY_DUMMY}.json")
        correct_render_artifact(output)
        assert isinstance(output.artifact[0].object, dict)
        assert output.artifact[0].filename == filename

    def test_get_lib_name(self, plugin):
        assert plugin().get_lib_name() == LIBRARY_DUMMY

    def test_get_lib_version(self, plugin):
        assert plugin().get_lib_version() == LIBRARY_DUMMY


class TestInferenceBuilderDummy:
    @pytest.fixture
    def plugin_builder(self, config_plugin_builder):
        return InferenceBuilderDummy(**config_plugin_builder)

    def test_build(self, plugin_builder):
        plugins = plugin_builder.build([RES_LOCAL_01])
        assert isinstance(plugins, list)
        assert len(plugins) == 1
        assert isinstance(plugins[0], InferencePluginDummy)
