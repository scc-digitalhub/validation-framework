"""
Run handler module.
"""
import concurrent.futures
from typing import Any, List

from datajudge.data_reader.base_file_reader import FileReader
from datajudge.plugins.plugin_factory import builder_factory
from datajudge.utils.commons import (OPERATION_INFERENCE,
                                     OPERATION_PROFILING, OPERATION_VALIDATION,
                                     RESULT_DATAJUDGE, RESULT_LIBRARY,
                                     RESULT_RENDERED, RESULT_WRAPPED)
from datajudge.utils.exceptions import RunError
from datajudge.utils.uri_utils import get_name_from_uri
from datajudge.utils.utils import flatten_list, listify


class RunHandlerRegistry:
    """
    Generic registry object to store objects
    based on operations.
    """

    def __init__(self) -> None:
        self.registry = {}
        self._setup()

    def _setup(self):
        """
        Setup the run handler registry.
        """
        for ops in [OPERATION_INFERENCE,
                    OPERATION_VALIDATION,
                    OPERATION_PROFILING]:
            self.registry[ops] = {}
            for res in [RESULT_WRAPPED,
                        RESULT_DATAJUDGE,
                        RESULT_RENDERED,
                        RESULT_LIBRARY]:
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
                 config: "RunConfig",
                 store_handler: "StoreHandler") -> None:

        self._config = config
        self._store_handler = store_handler
        self._registry = RunHandlerRegistry()

    def infer(self,
              resources: List["DataResource"],
              parallel: bool = False,
              num_worker: int = 10
              ) -> None:
        """
        Wrapper for plugins infer methods.
        """
        builders = builder_factory(self._config.inference,
                                   OPERATION_INFERENCE,
                                   self._store_handler.get_all_art_stores())
        plugins = self._create_plugins(builders, resources)
        self._scheduler(plugins, OPERATION_INFERENCE, parallel, num_worker)
        self._destroy_builders(builders)

    def validate(self,
                 resources: List["DataResource"],
                 constraints: List["Constraint"],
                 error_report: str,
                 parallel: bool = False,
                 num_worker: int = 10
                 ) -> None:
        """
        Wrapper for plugins validate methods.
        """
        if error_report not in ("count",
                                "partial",
                                "full"):
            raise RunError("Available options for error_report are 'count', 'partial', 'full'.")

        constraints = listify(constraints)
        builders = builder_factory(self._config.validation,
                                   OPERATION_VALIDATION,
                                   self._store_handler.get_all_art_stores())
        plugins = self._create_plugins(
            builders, resources, constraints, error_report)
        self._scheduler(plugins, OPERATION_VALIDATION, parallel, num_worker)
        self._destroy_builders(builders)

    def profile(self,
                resources: List["DataResource"],
                parallel: bool = False,
                num_worker: int = 10
                ) -> None:
        """
        Wrapper for plugins profile methods.
        """
        builders = builder_factory(self._config.profiling,
                                   OPERATION_PROFILING,
                                   self._store_handler.get_all_art_stores())
        plugins = self._create_plugins(builders, resources)
        self._scheduler(plugins, OPERATION_PROFILING, parallel, num_worker)
        self._destroy_builders(builders)

    @staticmethod
    def _create_plugins(builders: "PluginBuilder",
                        *args) -> List["Plugin"]:
        """
        Return a list of plugins.
        """
        return flatten_list([builder.build(*args) for builder in builders])

    def _scheduler(self,
                   plugins: List["Plugin"],
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
        for plugin in plugins:
            if plugin.exec_multiprocess and parallel:
                multiprocess.append(plugin)
            elif plugin.exec_multithread and parallel:
                multithreading.append(plugin)
            elif plugin.exec_distributed and parallel:
                distributed.append(plugin)
            else:
                sequential.append(plugin)

        # Revisite this
        self._sequential_execute(sequential, ops)
        self._pool_execute_multithread(multithreading, ops, num_worker)
        self._pool_execute_multiprocess(multiprocess, ops, num_worker)

    def _sequential_execute(self,
                            plugins: List["Plugin"],
                            ops: str) -> None:
        """
        Execute operations in sequence.
        """
        for plugin in plugins:
            data = self._execute(plugin)
            self._register_results(ops, data)

    def _pool_execute_multiprocess(self,
                                   plugins: List["Plugin"],
                                   ops: str,
                                   num_worker: int) -> None:
        """
        Instantiate a concurrent.future.ProcessPoolExecutor pool to
        execute operations in multiprocessing.
        """
        with concurrent.futures.ProcessPoolExecutor(max_workers=num_worker) as pool:
            for data in pool.map(self._execute, plugins):
                self._register_results(ops, data)

    def _pool_execute_multithread(self,
                                  plugins: List["Plugin"],
                                  ops: str,
                                  num_worker: int) -> None:
        """
        Instantiate a concurrent.future.ThreadPoolExecutor pool to
        execute operations in multithreading.
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_worker) as pool:
            for data in pool.map(self._execute, plugins):
                self._register_results(ops, data)

    @staticmethod
    def _execute(plugin: "Plugin") -> dict:
        """
        Wrap plugins main execution method. The handler create
        builders to build plugins. Once the plugin are built,
        the handler execute the main plugin operation
        (inference, validation or profiling), produce a datajudge
        report, render the execution artifact ready to be stored
        and save some library infos.
        """
        return plugin.execute()

    def _register_results(self,
                          operation: str,
                          result: dict,
                          ) -> None:
        """
        Register results.
        """
        for key, value in result.items():
            self._registry.register(operation, key, value)

    @staticmethod
    def _destroy_builders(builders: List["PluginBuilder"]) -> None:
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
        return [obj.artifact for obj in self.get_item(OPERATION_INFERENCE, RESULT_WRAPPED)]

    def get_artifact_report(self) -> List[Any]:
        """
        Get a list of reports produced by validation libraries.
        """
        return [obj.artifact for obj in self.get_item(OPERATION_VALIDATION, RESULT_WRAPPED)]

    def get_artifact_profile(self) -> List[Any]:
        """
        Get a list of profiles produced by profiling libraries.
        """
        return [obj.artifact for obj in self.get_item(OPERATION_PROFILING, RESULT_WRAPPED)]

    def get_datajudge_schema(self) -> List["DatajudgeSchema"]:
        """
        Wrapper for plugins parsing methods.
        """
        return [obj.artifact for obj in self.get_item(OPERATION_INFERENCE, RESULT_DATAJUDGE)]

    def get_datajudge_report(self) -> List["DatajudgeReport"]:
        """
        Wrapper for plugins parsing methods.
        """
        return [obj.artifact for obj in self.get_item(OPERATION_VALIDATION, RESULT_DATAJUDGE)]

    def get_datajudge_profile(self) -> List["DatajudgeProfile"]:
        """
        Wrapper for plugins parsing methods.
        """
        return [obj.artifact for obj in self.get_item(OPERATION_PROFILING, RESULT_DATAJUDGE)]

    def get_rendered_schema(self) -> List[Any]:
        """
        Get a list of schemas ready to be persisted.
        """
        return flatten_list([obj.artifact for obj in self.get_item(OPERATION_INFERENCE, RESULT_RENDERED)])

    def get_rendered_report(self) -> List[Any]:
        """
        Get a list of reports ready to be persisted.
        """
        return flatten_list([obj.artifact for obj in self.get_item(OPERATION_VALIDATION, RESULT_RENDERED)])

    def get_rendered_profile(self) -> List[Any]:
        """
        Get a list of profiles ready to be persisted.
        """
        return flatten_list([obj.artifact for obj in self.get_item(OPERATION_PROFILING, RESULT_RENDERED)])

    def get_libraries(self) -> List[dict]:
        """
        Return libraries used by run.
        """
        libs = {}
        for ops in [OPERATION_INFERENCE, OPERATION_PROFILING, OPERATION_VALIDATION]:
            libs[ops] = []
            for i in self.get_item(ops, RESULT_LIBRARY):
                if dict(**i) not in libs[ops]:
                    libs[ops].append(i)
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
                     resources: List["DataResource"],
                     dst: str) -> None:
        """
        Persist input data as artifact.
        """
        for res in resources:
            store = self._store_handler.get_art_store(res.store)
            data_reader = FileReader(store)
            for path in listify(res.path):
                tmp_pth = data_reader.fetch_data(path)
                filename = get_name_from_uri(tmp_pth)
                self.persist_artifact(tmp_pth, dst, filename, {})

    def clean_all(self) -> None:
        """
        Clean up.
        """
        self._store_handler.clean_all()
