"""
Run handler module.
"""
from __future__ import annotations

import concurrent.futures
import typing
from typing import Any, List

from datajudge.run.plugin.plugin_factory import builder_factory
from datajudge.utils.commons import (INFERENCE, PROFILING, VALIDATION,
                                     RES_WRAP, RES_DJ, RES_RENDER, RES_LIB)
from datajudge.utils.utils import flatten_list

if typing.TYPE_CHECKING:
    from datajudge.data.data_resource import DataResource
    from datajudge.data.datajudge_profile import DatajudgeProfile
    from datajudge.data.datajudge_report import DatajudgeReport
    from datajudge.data.datajudge_schema import DatajudgeSchema
    from datajudge.run.plugin.base_plugin import Plugin, PluginBuilder
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
                 config: RunConfig) -> None:

        self._config = config
        self._registry = RunHandlerRegistry()

    def infer(self,
              resources: List[DataResource],
              multithread: bool = False,
              num_worker: int = 10
              ) -> None:
        """
        Wrapper for plugins infer methods.
        """
        builders = builder_factory(self._config.inference, INFERENCE)
        plugins = self.create_plugins(builders, resources)
        if multithread:
            self.pool_execute(plugins, INFERENCE, num_worker)
        else:
            self.sequential_execute(plugins, INFERENCE)

    def validate(self,
                 resources: List[DataResource],
                 constraints: List[Constraint],
                 multithread: bool = False,
                 num_worker: int = 10
                 ) -> None:
        """
        Wrapper for plugins validate methods.
        """
        builders = builder_factory(self._config.validation, VALIDATION)
        plugins = self.create_plugins(builders, resources, constraints)
        if multithread:
            self.pool_execute(plugins, VALIDATION, num_worker)
        else:
            self.sequential_execute(plugins, VALIDATION)
        self.destroy_builders(builders)

    def profile(self,
                resources: List[DataResource],
                multithread: bool = False,
                num_worker: int = 10
                ) -> None:
        """
        Wrapper for plugins profile methods.
        """
        builders = builder_factory(self._config.profiling, PROFILING)
        plugins = self.create_plugins(builders, resources)
        if multithread:
            self.pool_execute(plugins, PROFILING, num_worker)
        else:
            self.sequential_execute(plugins, PROFILING)

    @staticmethod
    def create_plugins(builders: PluginBuilder, *args) -> List[Plugin]:
        """
        Return a list of plugins.
        """
        return flatten_list([builder.build(*args) for builder in builders])

    def sequential_execute(self,
                           plugins: List[Plugin],
                           ops: str) -> None:
        """
        Execute operations in sequence.
        """
        for plugin in plugins:
            data = self.execute(plugin)
            self.register_results(ops, data)

    def pool_execute(self,
                     plugins: List[Plugin],
                     ops: str,
                     num_worker: int) -> None:
        """
        Instantiate a multithreading pool to execute
        operations in parallel.
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
