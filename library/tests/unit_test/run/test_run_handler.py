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
    CONST_FRICT_01,
    METADATA_STORE_LOCAL,
    RES_LOCAL_01,
    RUN_CFG_EMPTY,
    STORE_LOCAL_01,
    Configurator,
)


class TestRunHandlerRegistry:
    @pytest.fixture()
    def registry(self):
        return RunHandlerRegistry()

    def test_setup(self, registry):
        res_dict_ = {
            RESULT_WRAPPED: [],
            RESULT_DATAJUDGE: [],
            RESULT_RENDERED: [],
            RESULT_LIBRARY: [],
        }
        dict_ = {
            OPERATION_PROFILING: res_dict_,
            OPERATION_INFERENCE: res_dict_,
            OPERATION_VALIDATION: res_dict_,
        }
        assert registry.registry == dict_

    def test_register(self, registry):
        registry.register(OPERATION_VALIDATION, RESULT_WRAPPED, ["test"])
        assert registry.registry[OPERATION_VALIDATION][RESULT_WRAPPED] == ["test"]
        registry.register(OPERATION_VALIDATION, RESULT_WRAPPED, "test2")
        assert registry.registry[OPERATION_VALIDATION][RESULT_WRAPPED] == [
            "test",
            "test2",
        ]
        registry.register(OPERATION_VALIDATION, RESULT_DATAJUDGE, "test3")
        assert registry.registry[OPERATION_VALIDATION][RESULT_DATAJUDGE] == ["test3"]

    def test_get_object(self, registry):
        print(registry.registry)
        registry.register(OPERATION_VALIDATION, RESULT_WRAPPED, ["test"])
        print(registry.registry)
        x = registry.get_object(OPERATION_VALIDATION, RESULT_WRAPPED)
        assert x == ["test"]
        x = registry.get_object("test", RESULT_WRAPPED)
        assert x == []


class TestRunHandler:
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
    def store_handler(self):
        return StoreHandler(
            metadata_store=self.md_loc_cfg_01, store=self.art_loc_cfg_01
        )

    @pytest.fixture()
    def handler(self, store_handler):
        return RunHandler(self.run_cfg, store_handler)

    def test_create_plugins(self, store_handler, handler):
        cfg = [self.run_cfg.inference, self.run_cfg.validation, self.run_cfg.profiling]
        ops = [OPERATION_INFERENCE, OPERATION_VALIDATION, OPERATION_PROFILING]
        stores = store_handler.get_all_art_stores()

        for i, j in zip(cfg, ops):
            builders = builder_factory(i, j, stores)
            if j == OPERATION_VALIDATION:
                plugins = handler._create_plugins(
                    builders, [RES_LOCAL_01], [CONST_FRICT_01], "full"
                )
            else:
                plugins = handler._create_plugins(builders, [RES_LOCAL_01])
            assert isinstance(plugins, list)
            for p in plugins:
                assert isinstance(p, Plugin)

    def test_parse_report_arg(self, handler):
        with pytest.raises(RunError):
            handler._parse_report_arg("")
        for i in ("count", "partial", "full"):
            assert handler._parse_report_arg(i) is None

    def test_register_results(self, handler):
        res = handler._register_results(OPERATION_INFERENCE, self.dict_result)
        assert res is None
        with pytest.raises(KeyError):
            handler._register_results("", self.dict_result)

    def test_destroy_builders(self, store_handler, handler):
        cfg = [self.run_cfg.inference, self.run_cfg.validation, self.run_cfg.profiling]
        ops = [OPERATION_INFERENCE, OPERATION_VALIDATION, OPERATION_PROFILING]
        stores = store_handler.get_all_art_stores()

        for i, j in zip(cfg, ops):
            builders = builder_factory(i, j, stores)
            assert handler._destroy_builders(builders) is None

    def test_get_item(self, handler):
        op = OPERATION_INFERENCE
        res = handler._register_results(op, self.dict_result)
        res = handler.get_item(op, RESULT_DATAJUDGE)
        assert isinstance(res[0], Result)

    def test_get_artifact_schema(self, handler):
        op = OPERATION_INFERENCE
        handler._register_results(op, self.dict_result)
        res = handler.get_artifact_schema()
        assert res[0] == "test"

    def test_get_artifact_report(self, handler):
        op = OPERATION_VALIDATION
        handler._register_results(op, self.dict_result)
        res = handler.get_artifact_report()
        assert res[0] == "test"

    def test_get_artifact_profile(self, handler):
        op = OPERATION_PROFILING
        handler._register_results(op, self.dict_result)
        res = handler.get_artifact_profile()
        assert res[0] == "test"

    def test_get_datajudge_schema(self, handler):
        op = OPERATION_INFERENCE
        handler._register_results(op, self.dict_result)
        res = handler.get_datajudge_schema()
        assert res[0] == "test"

    def test_get_datajudge_report(self, handler):
        op = OPERATION_VALIDATION
        handler._register_results(op, self.dict_result)
        res = handler.get_datajudge_report()
        assert res[0] == "test"

    def test_get_datajudge_profile(self, handler):
        op = OPERATION_PROFILING
        handler._register_results(op, self.dict_result)
        res = handler.get_datajudge_profile()
        assert res[0] == "test"

    def test_get_rendered_schema(self, handler):
        op = OPERATION_INFERENCE
        handler._register_results(op, self.dict_result)
        res = handler.get_rendered_schema()
        assert res[0] == "test"

    def test_get_rendered_report(self, handler):
        op = OPERATION_VALIDATION
        handler._register_results(op, self.dict_result)
        res = handler.get_rendered_report()
        assert res[0] == "test"

    def test_get_rendered_profile(self, handler):
        op = OPERATION_PROFILING
        handler._register_results(op, self.dict_result)
        res = handler.get_rendered_profile()
        assert res[0] == "test"

    def test_get_libraries(self, handler):
        op = OPERATION_PROFILING
        handler._register_results(op, self.dict_result)
        res = handler.get_libraries()
        assert res[op] == [{"test": "test"}]

    def test_log_metadata(self, handler):
        pth = Path(self.conf.get_tmp(), "report_0.json")
        handler.log_metadata(
            {"test": "test"}, pth.parent.as_posix(), MT_DJ_REPORT, True
        )
        assert pth.exists()
        with open(pth, "r") as f:
            assert f.read() == '{"test": "test"}'

    def test_persist_artifact(self, handler):
        pth = Path(self.conf.get_tmp(), "test.txt")
        handler.persist_artifact(
            {"test": "test"}, pth.parent.as_posix(), "test.txt", {}
        )
        assert pth.exists()
        with open(pth, "r") as f:
            assert f.read() == '{"test": "test"}'

    def test_persist_data(self, handler):
        handler.persist_data([RES_LOCAL_01], self.conf.get_tmp())
        assert Path(self.conf.get_tmp(), "test_csv_file.csv").exists()
