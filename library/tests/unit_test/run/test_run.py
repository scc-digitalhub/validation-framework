from pathlib import Path

import pytest

from datajudge.client.store_handler import StoreHandler
from datajudge.plugins.base_plugin import Plugin
from datajudge.plugins.plugin_factory import builder_factory
from datajudge.plugins.utils.plugin_utils import Result
from datajudge.run.run import Run
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


class TestRun:
    def test_log_run(self, handler, temp_data):
        pth = Path(temp_data, "report_0.json")
        handler.log_metadata({"test": "test"}, str(pth.parent), MT_DJ_REPORT, True)
        assert pth.exists()
        with open(pth, "r") as f:
            assert f.read() == '{"test": "test"}'

    def test_log_env(self, handler, temp_data):
        pth = Path(temp_data, "report_0.json")
        handler.log_metadata({"test": "test"}, str(pth.parent), MT_DJ_REPORT, True)
        assert pth.exists()
        with open(pth, "r") as f:
            assert f.read() == '{"test": "test"}'

    def test_get_blob(self, handler):
        pass

    def test_log_metadata(self, handler, temp_data):
        pth = Path(temp_data, "report_0.json")
        handler.log_metadata({"test": "test"}, str(pth.parent), MT_DJ_REPORT, True)
        assert pth.exists()
        with open(pth, "r") as f:
            assert f.read() == '{"test": "test"}'

    def test_get_artifact_metadata(self, handler):
        pass

    def test_persist_artifact(self, handler, temp_data):
        pth = Path(temp_data, "test.txt")
        handler.persist_artifact({"test": "test"}, str(pth.parent), "test.txt", {})
        assert pth.exists()
        with open(pth, "r") as f:
            assert f.read() == '{"test": "test"}'

    def test_render_artifact_name(self, handler):
        pass

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

    def test_persist_data(self, handler, local_resource, tmp_path):
        # Use another tmp path, otherways raise SameFileError
        # because copy same file to same path (from temp_data to temp_data)
        handler.persist_data([local_resource], tmp_path)
        assert Path(tmp_path, "test_csv_file.csv").exists()


# RunHandlerRegistry
@pytest.fixture()
def registry():
    return RunHandlerRegistry()


# StoreHandler
@pytest.fixture()
def store_handler(local_md_store_cfg, local_store_cfg):
    return StoreHandler(metadata_store=local_md_store_cfg, store=local_store_cfg)


# RunHandler
@pytest.fixture()
def handler(run_empty, store_handler):
    return RunHandler(run_empty, store_handler)


# Sample result dict
@pytest.fixture()
def dict_result(result_obj):
    return {
        RESULT_WRAPPED: result_obj,
        RESULT_DATAJUDGE: result_obj,
        RESULT_RENDERED: result_obj,
        RESULT_LIBRARY: [{"test": "test"}],
    }
