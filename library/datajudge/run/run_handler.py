"""
Run handler module.
"""
from __future__ import annotations

import typing
from typing import Any, List

from datajudge.run.plugin.plugin_factory import get_builder
from datajudge.utils.commons import (OP_INF, OP_PRO, OP_VAL,
                                     RES_WRAP, RES_DJ,
                                     RES_RENDER, RES_LIB)
from datajudge.utils.utils import flatten_list

if typing.TYPE_CHECKING:
    from datajudge.data.data_resource import DataResource
    from datajudge.data.datajudge_profile import DatajudgeProfile
    from datajudge.data.datajudge_report import DatajudgeReport
    from datajudge.data.datajudge_schema import DatajudgeSchema
    from datajudge.run.plugin.base_plugin import Plugin, PluginBuilder
    from datajudge.run.plugin.plugin_utils import Result
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
        for ops in [OP_INF, OP_VAL, OP_PRO]:
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

    def infer(self, resources: List[DataResource]) -> None:
        """
        Wrapper for plugins infer methods.
        """
        builders = get_builder(self._config.inference, OP_INF)
        plugins = [builder.build(resources) for builder in builders]
        self.execute(plugins, OP_INF)
        self.destroy(builders)

    def validate(self,
                 resources: List[DataResource],
                 constraints: List[Constraint]
                 ) -> None:
        """
        Wrapper for plugins validate methods.
        """
        builders = get_builder(self._config.validation, OP_VAL)
        plugins = [builder.build(resources, constraints) for builder in builders]
        self.execute(plugins, OP_VAL)
        self.destroy(builders)

    def profile(self, resources: List[DataResource]) -> None:
        """
        Wrapper for plugins profile methods.
        """
        builders = get_builder(self._config.profiling, OP_PRO)
        plugins = [builder.build(resources) for builder in builders]
        self.execute(plugins, OP_PRO)
        self.destroy(builders)

    def execute(self,
                plugins: List[List[Plugin]],
                operation: str,
                ) -> None:
        """
        Wrap plugins main execution method. The handler create
        builders to build plugins. Once the plugin are built,
        the handler execute the main plugin operation
        (inference, validation or profiling), produce a datajudge
        report, render the execution artifact ready to be stored
        and save some library infos.
        """
        for plugin in flatten_list(plugins):
            results = plugin.execute()
            self.register_results(operation, results)

    def register_results(self,
                         operation: str,
                         result: dict,
                         ) -> None:
        """
        Register results.
        """
        for key, value in result.items():
            self._registry.register(operation, key, value)

    def destroy(self, builders: PluginBuilder) -> None:
        """
        Destroy builders.
        """
        for builder in builders:
            try:
                builder.cleanup()
            except:
                pass

    def get_item(self, operation: str, _type: str) -> List[Any]:
        """
        Get item from registry.
        """
        return self._registry.get_object(operation, _type)

    def get_artifact_schema(self) -> List[Any]:
        """
        Get a list of schemas produced by inference libraries.
        """
        return [obj.artifact for obj in self.get_item(OP_INF, RES_WRAP)]

    def get_artifact_report(self) -> List[Any]:
        """
        Get a list of reports produced by validation libraries.
        """
        return [obj.artifact for obj in self.get_item(OP_VAL, RES_WRAP)]

    def get_artifact_profile(self) -> List[Any]:
        """
        Get a list of profiles produced by profiling libraries.
        """
        return [obj.artifact for obj in self.get_item(OP_PRO, RES_WRAP)]

    def get_datajudge_schema(self) -> List[DatajudgeSchema]:
        """
        Wrapper for plugins parsing methods.
        """
        return [obj.artifact for obj in self.get_item(OP_INF, RES_DJ)]

    def get_datajudge_report(self) -> List[DatajudgeReport]:
        """
        Wrapper for plugins parsing methods.
        """
        return [obj.artifact for obj in self.get_item(OP_VAL, RES_DJ)]

    def get_datajudge_profile(self) -> List[DatajudgeProfile]:
        """
        Wrapper for plugins parsing methods.
        """
        return [obj.artifact for obj in self.get_item(OP_PRO, RES_DJ)]

    def get_rendered_schema(self) -> List[Any]:
        """
        Get a list of schemas ready to be persisted.
        """
        return flatten_list([obj.artifact for obj in self.get_item(OP_INF, RES_RENDER)])

    def get_rendered_report(self) -> List[Any]:
        """
        Get a list of reports ready to be persisted.
        """
        return flatten_list([obj.artifact for obj in self.get_item(OP_VAL, RES_RENDER)])

    def get_rendered_profile(self) -> List[Any]:
        """
        Get a list of profiles ready to be persisted.
        """
        return flatten_list([obj.artifact for obj in self.get_item(OP_PRO, RES_RENDER)])
