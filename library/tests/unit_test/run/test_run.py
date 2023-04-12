from datajudge.run.run import Run
from pathlib import Path

import pytest

from datajudge.client.store_handler import StoreHandler
from datajudge.plugins.base_plugin import Plugin
from datajudge.plugins.plugin_factory import builder_factory
from datajudge.plugins.utils.plugin_utils import Result
from datajudge.run.run_handler import RunHandler, RunHandlerRegistry
from datajudge.utils.commons import (
    MT_DJ_REPORT,
    OPERATION_INFERENCE,
    OPERATION_PROFILING,
    OPERATION_VALIDATION,
    RESULT_DATAJUDGE,
    RESULT_LIBRARY,
    RESULT_RENDERED,
    RESULT_WRAPPED,
)
from datajudge.utils.exceptions import RunError
from tests.conftest import (
    METADATA_STORE_LOCAL,
    RES_LOCAL_01,
    RUN_CFG_EMPTY,
    STORE_LOCAL_01,
    Configurator,
)


class TestRun:
    run_cfg = RUN_CFG_EMPTY
    conf = Configurator()
    md_loc_cfg_01 = conf.get_store_cfg(METADATA_STORE_LOCAL, tmp=True)
    art_loc_cfg_01 = conf.get_store_cfg(STORE_LOCAL_01, tmp=True)
    result = conf.get_result_test()
    dict_result = {
        RESULT_WRAPPED: result,
        RESULT_DATAJUDGE: result,
        RESULT_RENDERED: result,
        RESULT_LIBRARY: [{"test": "test"}],
    }

    @pytest.fixture()
    def handler(self):
        store_handler = StoreHandler(
            metadata_store=self.md_loc_cfg_01, store=self.art_loc_cfg_01
        )
        return RunHandler(self.run_cfg, store_handler)

    def test_log_run(self, handler):
        pth = Path(self.conf.get_tmp(), "report_0.json")
        handler.log_metadata(
            {"test": "test"}, pth.parent.as_posix(), MT_DJ_REPORT, True
        )
        assert pth.exists()
        with open(pth, "r") as f:
            assert f.read() == '{"test": "test"}'

    def test_log_env(self, handler):
        pth = Path(self.conf.get_tmp(), "report_0.json")
        handler.log_metadata(
            {"test": "test"}, pth.parent.as_posix(), MT_DJ_REPORT, True
        )
        assert pth.exists()
        with open(pth, "r") as f:
            assert f.read() == '{"test": "test"}'

    def test_get_blob(self, handler):
        pass

    def test_log_metadata(self, handler):
        pth = Path(self.conf.get_tmp(), "report_0.json")
        handler.log_metadata(
            {"test": "test"}, pth.parent.as_posix(), MT_DJ_REPORT, True
        )
        assert pth.exists()
        with open(pth, "r") as f:
            assert f.read() == '{"test": "test"}'

    def test_get_artifact_metadata(self, handler):
        pass

    def test_log_artifact(self, handler):
        pth = Path(self.conf.get_tmp(), "report_0.json")
        handler.log_metadata(
            {"test": "test"}, pth.parent.as_posix(), MT_DJ_REPORT, True
        )
        assert pth.exists()
        with open(pth, "r") as f:
            assert f.read() == '{"test": "test"}'

    def test_render_artifact_name(self, handler):
        pass

    def test_persist_artifact(self, handler):
        pth = Path(self.conf.get_tmp(), "test.txt")
        handler.persist_artifact(
            {"test": "test"}, pth.parent.as_posix(), "test.txt", {}
        )
        assert pth.exists()
        with open(pth, "r") as f:
            assert f.read() == '{"test": "test"}'

    def test_check_metadata_uri(self, handler):
        pass

    def test_check_artifacts_uri(self, handler):
        pass

    def test_get_libraries(self, handler):
        pass

    def test_infer_wrapper(self, handler):
        pass

    def test_infer_datajudge(self, handler):
        pass

    def test_infer(self, handler):
        pass

    def test_log_schema(self, handler):
        pass

    def test_persist_schema(self, handler):
        pass

    def test_validate_wrapper(self, handler):
        pass

    def test_validate_datajudge(self, handler):
        pass

    def test_validate(self, handler):
        pass

    def test_log_report(self, handler):
        pass

    def test_persist_report(self, handler):
        pass

    def test_profile_wrapper(self, handler):
        pass

    def test_profile_datajudge(self, handler):
        pass

    def test_profile(self, handler):
        pass

    def test_log_profile(self, handler):
        pass

    def test_persist_profile(self, handler):
        pass

    def test_persist_data(self, handler):
        handler.persist_data([RES_LOCAL_01], self.conf.get_tmp())
        assert Path(self.conf.get_tmp(), "test_csv_file.csv").exists()
