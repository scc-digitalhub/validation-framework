"""
Run handler module.
"""
from __future__ import annotations

import concurrent.futures
import typing
from copy import deepcopy
from typing import Any, List

from datajudge.run.plugin.plugin_factory import builder_factory
from datajudge.utils.commons import (INFERENCE, PROFILING, VALIDATION,
                                     RES_WRAP, RES_DJ, RES_RENDER, RES_LIB)
from datajudge.utils.uri_utils import get_name_from_uri
from datajudge.utils.utils import flatten_list, listify

if typing.TYPE_CHECKING:
    from datajudge.data.data_resource import DataResource
    from datajudge.data.datajudge_profile import DatajudgeProfile
    from datajudge.data.datajudge_report import DatajudgeReport
    from datajudge.data.datajudge_schema import DatajudgeSchema
    from datajudge.run.plugin.base_plugin import Plugin, PluginBuilder
    from datajudge.client.store_handler import StoreHandler
    from datajudge.utils.config import Constraint, RunConfig


class RunHandlerRegistry:
    """
    Generic registry object to store objects
    based on operations.
    """
    def __init__(self) -> None:
        self.registry = {}
        self.setup()

    def setup(self):
        """
        Setup the run handler registry.
        """
        for ops in [INFERENCE, VALIDATION, PROFILING]:
            self.registry[ops] = {}
            for res in [RES_WRAP, RES_DJ, RES_RENDER, RES_LIB]:
                self.registry[ops][res] = []

    def register(self,
                 ops: str,
                 _type: str,
                 _object: Any
                 ) -> None:
        """
        Register an object on the registry based on
        operation and result typology.
        """
        if isinstance(_object, list):
            self.registry[ops][_type].extend(_object)
        else:
            self.registry[ops][_type].append(_object)

    def get_object(self,
                   ops: str,
                   _type: str) -> list:
        """
        Return object from registry.
        """
        try:
            return self.registry[ops][_type]
        except KeyError:
            return []


class RunHandler:
    """
    Run handler.

    This class create a layer of abstraction between the Run
    and its plugins.

    """

    def __init__(self,
                 config: RunConfig,
                 store_handler: StoreHandler) -> None:

        self._config = config
        self._store_handler = store_handler
        self._registry = RunHandlerRegistry()

    def infer(self,
              resources: List[DataResource],
              parallel: bool = False,
              num_worker: int = 10
              ) -> None:
        """
        Wrapper for plugins infer methods.
        """
        builders = builder_factory(self._config.inference,
                                   INFERENCE,
                                   self._store_handler.get_all_art_stores())
        plugins = self.create_plugins(builders, resources)
        self.scheduler(plugins, INFERENCE, parallel, num_worker)

    def validate(self,
                 resources: List[DataResource],
                 constraints: List[Constraint],
                 parallel: bool = False,
                 num_worker: int = 10
                 ) -> None:
        """
        Wrapper for plugins validate methods.
        """
        builders = builder_factory(self._config.validation,
                                   VALIDATION,
                                   self._store_handler.get_all_art_stores())
        plugins = self.create_plugins(builders, resources, constraints)
        self.scheduler(plugins, VALIDATION, parallel, num_worker)
        self.destroy_builders(builders)

    def profile(self,
                resources: List[DataResource],
                parallel: bool = False,
                num_worker: int = 10
                ) -> None:
        """
        Wrapper for plugins profile methods.
        """
        builders = builder_factory(self._config.profiling,
                                   PROFILING,
                                   self._store_handler.get_all_art_stores())
        plugins = self.create_plugins(builders, resources)
        self.scheduler(plugins, PROFILING, parallel, num_worker)

    @staticmethod
    def create_plugins(builders: PluginBuilder,
                       *args) -> List[Plugin]:
        """
        Return a list of plugins.
        """
        return flatten_list([builder.build(*args) for builder in builders])

    def scheduler(self,
                  plugins: List[Plugin],
                  ops: str,
                  parallel: bool,
                  num_worker: int) -> None:
        """
        Schedule execution to avoid multiprocessing issues.
        """
        multiprocess = []
        multithreading = []
        distributed = []
        sequential = []
        for p in plugins:
            if p.exec_multiprocess and parallel:
                multiprocess.append(p)
            elif p.exec_multithread and parallel:
                multithreading.append(p)
            elif p.exec_distributed and parallel:
                distributed.append(p)
            else:
                sequential.append(p)

        # Revisite this
        self.sequential_execute(sequential, ops)
        self.pool_execute_multithread(multithreading, ops, num_worker)
        self.pool_execute_multiprocess(multiprocess, ops, num_worker)

    def sequential_execute(self,
                           plugins: List[Plugin],
                           ops: str) -> None:
        """
        Execute operations in sequence.
        """
        for plugin in plugins:
            data = self.execute(plugin)
            self.register_results(ops, data)

    def pool_execute_multiprocess(self,
                                  plugins: List[Plugin],
                                  ops: str,
                                  num_worker: int) -> None:
        """
        Instantiate a concurrent.future.ProcessPoolExecutor pool to
        execute operations in multiprocessing.
        """
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_worker) as pool:
            for data in pool.map(self.execute, plugins):
                self.register_results(ops, data)

    def pool_execute_multithread(self,
                                 plugins: List[Plugin],
                                 ops: str,
                                 num_worker: int) -> None:
        """
        Instantiate a concurrent.future.ThreadPoolExecutor pool to
        execute operations in multithreading.
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_worker) as pool:
            for data in pool.map(self.execute, plugins):
                self.register_results(ops, data)

    def execute(self, plugin: Plugin) -> dict:
        """
        Wrap plugins main execution method. The handler create
        builders to build plugins. Once the plugin are built,
        the handler execute the main plugin operation
        (inference, validation or profiling), produce a datajudge
        report, render the execution artifact ready to be stored
        and save some library infos.
        """
        return plugin.execute()

    def register_results(self,
                         operation: str,
                         result: dict,
                         ) -> None:
        """
        Register results.
        """
        for key, value in result.items():
            self._registry.register(operation, key, value)

    def destroy_builders(self,
                         builders: List[PluginBuilder]) -> None:
        """
        Destroy builders.
        """
        for builder in builders:
            builder.destroy()

    def get_item(self, operation: str, _type: str) -> List[Any]:
        """
        Get item from registry.
        """
        return self._registry.get_object(operation, _type)

    def get_artifact_schema(self) -> List[Any]:
        """
        Get a list of schemas produced by inference libraries.
        """
        return [obj.artifact for obj in self.get_item(INFERENCE, RES_WRAP)]

    def get_artifact_report(self) -> List[Any]:
        """
        Get a list of reports produced by validation libraries.
        """
        return [obj.artifact for obj in self.get_item(VALIDATION, RES_WRAP)]

    def get_artifact_profile(self) -> List[Any]:
        """
        Get a list of profiles produced by profiling libraries.
        """
        return [obj.artifact for obj in self.get_item(PROFILING, RES_WRAP)]

    def get_datajudge_schema(self) -> List[DatajudgeSchema]:
        """
        Wrapper for plugins parsing methods.
        """
        return [obj.artifact for obj in self.get_item(INFERENCE, RES_DJ)]

    def get_datajudge_report(self) -> List[DatajudgeReport]:
        """
        Wrapper for plugins parsing methods.
        """
        return [obj.artifact for obj in self.get_item(VALIDATION, RES_DJ)]

    def get_datajudge_profile(self) -> List[DatajudgeProfile]:
        """
        Wrapper for plugins parsing methods.
        """
        return [obj.artifact for obj in self.get_item(PROFILING, RES_DJ)]

    def get_rendered_schema(self) -> List[Any]:
        """
        Get a list of schemas ready to be persisted.
        """
        return flatten_list([obj.artifact for obj in self.get_item(INFERENCE, RES_RENDER)])

    def get_rendered_report(self) -> List[Any]:
        """
        Get a list of reports ready to be persisted.
        """
        return flatten_list([obj.artifact for obj in self.get_item(VALIDATION, RES_RENDER)])

    def get_rendered_profile(self) -> List[Any]:
        """
        Get a list of profiles ready to be persisted.
        """
        return flatten_list([obj.artifact for obj in self.get_item(PROFILING, RES_RENDER)])

    def get_libraries(self) -> List[dict]:
        """
        Return libraries used by run.
        """
        libs = {}
        for op in [INFERENCE, PROFILING, VALIDATION]:
            libs[op] = []
            for i in self.get_item(op, RES_LIB):
                if dict(**i) not in libs[op]:
                    libs[op].append(i)
        return libs

    def log_metadata(self,
                     src: dict,
                     dst: str,
                     src_type: str,
                     overwrite: bool) -> None:
        """
        Method to log metadata in the metadata store.
        """
        store = self._store_handler.get_md_store()
        store.log_metadata(src, dst, src_type, overwrite)

    def persist_artifact(self,
                         src: Any,
                         dst: str,
                         src_name: str,
                         metadata: dict) -> None:
        """
        Method to persist artifacts in the default artifact store.
        """
        store = self._store_handler.get_def_store()
        store.persist_artifact(src, dst, src_name, metadata)

    def persist_data(self,
                     resources: List[DataResource],
                     file_format: str,
                     dst: str) -> None:
        """
        Persist input data as artifact.
        """
        for res in resources:
            resource = deepcopy(res)
            for store in self._store_handler.get_all_art_stores():
               if store.name == resource.store:
                    resource.tmp_pth = store.fetch_artifact(resource.path,
                                                            file_format)

            for path in listify(resource.tmp_pth):
                filename = get_name_from_uri(path)
                self.persist_artifact(path, dst, filename, {})

    def clean_all(self) -> None:
        """
        Clean up.
        """
        self._store_handler.clean_all()
