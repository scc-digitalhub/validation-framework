"""
Run handler module.
"""
from __future__ import annotations

import typing
from typing import Any, List, Optional

from datajudge.run.plugin.plugin_factory import get_builder
from datajudge.utils import config as cfg

if typing.TYPE_CHECKING:
    from datajudge import DataResource
    from datajudge.utils.config import RunConfig


OBJ_RES = "results"
OBJ_REP = "dj_reports"
OBJ_ART = "rendered_artifacts"
OBJ_LIB = "libraries"


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
        for ops in [cfg.OP_VAL, cfg.OP_PRO, cfg.OP_INF]:
            self.registry[ops] = {
                OBJ_RES: [],
                OBJ_REP: [],
                OBJ_ART: [],
                OBJ_LIB: []
            }

    def register(self,
                 ops: str,
                 obj_typ: str,
                 _object: Any) -> None:
        """
        Register an object on the registry.
        """
        if isinstance(_object, list):
            self.registry[ops][obj_typ].extend(_object)
        else:
            self.registry[ops][obj_typ].append(_object)

    def get_object(self,
                   ops: str,
                   obj_typ: str) -> List[Any]:
        """
        Return object from registry.
        """
        try:
            return self.registry[ops][obj_typ]
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
              exec_args: Optional[dict] = None
              ) -> list:
        """
        Wrapper for plugins infer methods.
        """
        self.execute(cfg.OP_INF, resources, exec_args)

    def validate(self,
                 resources: List[DataResource],
                 constraints: dict,
                 exec_args: Optional[dict] = None
                 ) -> list:
        """
        Wrapper for plugins validate methods.
        """
        self.execute(cfg.OP_VAL, resources, exec_args, constraints)

    def profile(self,
                resources: List[DataResource],
                exec_args: Optional[dict] = None
                ) -> None:
        """
        Wrapper for plugins profile methods.
        """
        self.execute(cfg.OP_PRO, resources, exec_args)

    def execute(self,
                operation: str,
                resources: List[DataResource],
                exec_args: Optional[dict] = None,
                constraints: Optional[dict] = None
                ) -> None:
        """
        Wrap plugin main execution method.
        """
        if exec_args is None:
            exec_args = {}

        builder_cfg = self._config.dict().get(operation)
        builders = get_builder(builder_cfg, operation)

        plugins = []
        for _, builder in builders.items():
            if operation == cfg.OP_VAL:
                plugins.extend(builder.build(resources, exec_args, constraints))
            else:
                plugins.extend(builder.build(resources, exec_args))

        for plugin in plugins:
            result = plugin.execute()
            self._registry.register(operation, OBJ_RES, result)

            dj_report = plugin.render_datajudge(result)
            self._registry.register(operation, OBJ_REP, dj_report)

            rendered_artifact = plugin.render_artifact(result.artifact)
            self._registry.register(operation, OBJ_ART, rendered_artifact)
            
            libraries = plugin.get_library()
            self._registry.register(operation, OBJ_LIB, libraries)

    def get_result_schema(self) -> list:
        """
        Render a list of schemas to be persisted.
        """
        res = []
        for obj in self._registry.get_object(cfg.OP_INF, OBJ_RES):
            res.append(obj.artifact)
        return res

    def get_result_report(self) -> list:
        """
        Render a list of reports to be persisted.
        """
        res = []
        for obj in self._registry.get_object(cfg.OP_VAL, OBJ_RES):
            res.append(obj.artifact)
        return res

    def get_result_profile(self) -> list:
        """
        Render a list of profiles to be persisted.
        """
        res = []
        for obj in self._registry.get_object(cfg.OP_PRO, OBJ_RES):
            res.append(obj.artifact)
        return res

    def get_datajudge_schema(self) -> list:
        """
        Wrapper for plugins parsing methods.
        """
        return self._registry.get_object(cfg.OP_INF, OBJ_REP)

    def get_datajudge_report(self) -> list:
        """
        Wrapper for plugins parsing methods.
        """
        return self._registry.get_object(cfg.OP_VAL, OBJ_REP)

    def get_datajudge_profile(self) -> list:
        """
        Wrapper for plugins parsing methods.
        """
        return self._registry.get_object(cfg.OP_PRO, OBJ_REP)

    def get_artifact_schema(self) -> list:
        """
        Render a list of schemas to be persisted.
        """
        return self._registry.get_object(cfg.OP_INF, OBJ_ART)

    def get_artifact_report(self) -> list:
        """
        Render a list of reports to be persisted.
        """
        return self._registry.get_object(cfg.OP_VAL, OBJ_ART)

    def get_artifact_profile(self) -> list:
        """
        Render a list of profiles to be persisted.
        """
        return self._registry.get_object(cfg.OP_PRO, OBJ_ART)
