"""
Run handler module.
"""
from __future__ import annotations

import typing
from typing import Any, List, Union
from datajudge.data.datajudge_profile import DatajudgeProfile
from datajudge.data.datajudge_report import DatajudgeReport
from datajudge.data.datajudge_schema import DatajudgeSchema

from datajudge.run.plugin.plugin_factory import get_builder
from datajudge.utils import config as cfg
from datajudge.utils.utils import flatten_list

if typing.TYPE_CHECKING:
    from datajudge.data.data_resource import DataResource
    from datajudge.run.plugin.base_plugin import Plugin, Result
    from datajudge.utils.config import RunConfig, Constraint


# Objects

OBJ_RES = "results"
OBJ_REP = "dj_reports"
OBJ_ART = "rendered_artifacts"
OBJ_LIB = "libraries"

# Operations

_INF = cfg.OP_INF
_VAL = cfg.OP_VAL
_PRO = cfg.OP_PRO


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
        for operation in [_INF, _VAL, _PRO]:
            self.registry[operation] = []

    def register(self,
                 operation: str,
                 _object: Union[Result, List[Result]]
                 ) -> None:
        """
        Register an object on the registry.
        """
        if isinstance(_object, list):
            self.registry[operation].extend(_object)
        else:
            self.registry[operation].append(_object)

    def get_object(self,
                   operation: str) -> List[Result]:
        """
        Return object from registry.
        """
        try:
            return self.registry[operation]
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
        builders = get_builder(self._config.inference, _INF)
        plugins = [builder.build(resources) for builder in builders]
        self.execute(plugins, _INF)

    def validate(self,
                 resources: List[DataResource],
                 constraints: List[Constraint]
                 ) -> None:
        """
        Wrapper for plugins validate methods.
        """
        builders = get_builder(self._config.validation, _VAL)
        plugins = [builder.build(resources, constraints) for builder in builders]
        self.execute(plugins, _VAL)

    def profile(self, resources: List[DataResource]) -> None:
        """
        Wrapper for plugins profile methods.
        """
        builders = get_builder(self._config.profiling, _PRO)
        plugins = [builder.build(resources) for builder in builders]
        self.execute(plugins, _PRO)

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
            result = plugin.execute()
            self.register_results(operation, result)

    def register_results(self,
                         operation: str,
                         result: Result,
                         ) -> None:
        """
        Register results.
        """
        self._registry.register(operation, result)

    def get_item(self, operation: str) -> List[Any]:
        """
        Get item from registry.
        """
        return self._registry.get_object(operation)

    def get_artifact_schema(self) -> List[Any]:
        """
        Get a list of schemas produced by inference libraries.
        """
        return [obj.artifact for obj in self.get_item(_INF)]

    def get_artifact_report(self) -> List[Any]:
        """
        Get a list of reports produced by validation libraries.
        """
        return [obj.artifact for obj in self.get_item(_VAL)]

    def get_artifact_profile(self) -> List[Any]:
        """
        Get a list of profiles produced by profiling libraries.
        """
        return [obj.artifact for obj in self.get_item(_PRO)]

    def get_datajudge_schema(self) -> List[DatajudgeSchema]:
        """
        Wrapper for plugins parsing methods.
        """
        return [obj.datajudge_artifact for obj in self.get_item(_INF)]

    def get_datajudge_report(self) -> List[DatajudgeReport]:
        """
        Wrapper for plugins parsing methods.
        """
        return [obj.datajudge_artifact for obj in self.get_item(_VAL)]

    def get_datajudge_profile(self) -> List[DatajudgeProfile]:
        """
        Wrapper for plugins parsing methods.
        """
        return [obj.datajudge_artifact for obj in self.get_item(_PRO)]

    def get_rendered_schema(self) -> List[Any]:
        """
        Get a list of schemas ready to be persisted.
        """
        return flatten_list([obj.rendered_artifact for obj in self.get_item(_INF)])

    def get_rendered_report(self) -> List[Any]:
        """
        Get a list of reports ready to be persisted.
        """
        return flatten_list([obj.rendered_artifact for obj in self.get_item(_VAL)])

    def get_rendered_profile(self) -> List[Any]:
        """
        Get a list of profiles ready to be persisted.
        """
        return flatten_list([obj.rendered_artifact for obj in self.get_item(_PRO)])

