from datajudge.plugins.utils.plugin_utils import Result, exec_decorator
from datajudge.utils.commons import (
    RESULT_DATAJUDGE,
    RESULT_LIBRARY,
    RESULT_RENDERED,
    RESULT_WRAPPED,
)
from datajudge.plugins.profiling.profiling_plugin import Profiling


class SamplePlugin(Profiling):
    """
    Sample concrete plugin implementation for testing.
    """

    def setup(self, *args, **kwargs) -> None:
        ...

    @exec_decorator
    def profile(self) -> dict:
        return {"result": "success"}

    @exec_decorator
    def render_datajudge(self, obj: "Result") -> "Result":
        return obj  # dummy implementation for testing

    @exec_decorator
    def render_artifact(self, obj: "Result") -> "Result":
        return obj  # dummy implementation for testing

    @staticmethod
    def get_lib_name() -> str:
        return "SamplePlugin"

    @staticmethod
    def get_lib_version() -> str:
        return "1.0"


class TestProfile:
    def test_execute(self, caplog):
        plugin = SamplePlugin()
        plugin._id = "test"
        result = plugin.execute()

        assert isinstance(result, dict)

        keys = [RESULT_WRAPPED, RESULT_DATAJUDGE, RESULT_RENDERED, RESULT_LIBRARY]
        for k in keys:
            assert k in result

        assert isinstance(result[RESULT_WRAPPED], Result)
        assert isinstance(result[RESULT_DATAJUDGE], Result)
        assert isinstance(result[RESULT_RENDERED], Result)
        assert isinstance(result[RESULT_LIBRARY], dict)
        lib = {"libraryName": "SamplePlugin", "libraryVersion": "1.0"}
        assert result[RESULT_LIBRARY] == lib

        plg = f"Plugin: SamplePlugin {plugin._id};"
        assert f"Execute profiling - {plg}" in caplog.text
        assert f"Render report - {plg}" in caplog.text
        assert f"Render artifact - {plg}" in caplog.text
