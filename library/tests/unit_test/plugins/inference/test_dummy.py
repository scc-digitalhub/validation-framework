import pytest

from datajudge.plugins.inference.dummy_inference import (
    InferenceBuilderDummy,
    InferencePluginDummy,
)
from datajudge.utils.commons import LIBRARY_DUMMY, OPERATION_INFERENCE, BASE_FILE_READER
from tests.unit_test.plugins.utils_plugin_tests import (
    correct_execute,
    correct_render_artifact,
    correct_render_datajudge,
)


class TestInferencePluginDummy:
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
    def test_build(self, plugin_builder, plugin_builder_non_val_args):
        plugins = plugin_builder.build(*plugin_builder_non_val_args)
        assert isinstance(plugins, list)
        assert len(plugins) == 1
        assert isinstance(plugins[0], InferencePluginDummy)


@pytest.fixture(scope="module")
def plugin():
    return InferencePluginDummy


@pytest.fixture
def plugin_builder(config_plugin_builder):
    return InferenceBuilderDummy(**config_plugin_builder)


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
