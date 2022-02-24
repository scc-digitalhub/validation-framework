"""
Run plugins registry module.
"""
from __future__ import annotations
from dataclasses import dataclass

import typing
from typing import Any, List

from datajudge.run.plugin.plugin_factory import get_plugin

if typing.TYPE_CHECKING:
    from datajudge import RunConfig


@dataclass
class ArtifactWrapper:
    res_name: str
    library: str
    result: Any
    outcome: str


class PluginHandler:
    
    def __init__(self,
                 inference_plugin: Any,
                 validation_plugin: Any,
                 profiling_plugin: Any) -> None:

        self._inference_plugins = inference_plugin
        self._validation_plugins = validation_plugin
        self._profiling_plugins = profiling_plugin

    def infer(self, *args, **kwargs) -> List[ArtifactWrapper]:
        """
        Wrapper for plugins infer methods.
        """
        return self.execute(self.inf, *args, **kwargs)

    def validate(self, *args, **kwargs) -> List[ArtifactWrapper]:
        """
        Wrapper for plugins validate methods.
        """
        return self.execute(self.val, *args, **kwargs)
    
    def profile(self, *args, **kwargs) -> List[ArtifactWrapper]:
        """
        Wrapper for plugins profile methods.
        """
        return self.execute(self.pro, *args, **kwargs)

    def execute(self, plugin: Any, *args, **kwargs) -> List[ArtifactWrapper]:
        """
        Wrap plugin main execution method.
        """
        # Weak
        res_name = args[0]
        
        results = []
        for lib in plugin:
            library = plugin[lib].lib_name
            result = plugin[lib].execute(*args, **kwargs)
            outcome = plugin[lib].get_outcome(result)
            results.append(ArtifactWrapper(res_name, library, result, outcome))
        return results

    def produce_schema(self, objects: List[ArtifactWrapper]) -> dict:
        """
        Wrapper for plugins parsing methods.
        """
        return self.produce_log(self.inf, objects)

    def produce_report(self, objects: List[ArtifactWrapper]) -> dict:
        """
        Wrapper for plugins parsing methods.
        """
        return self.produce_log(self.val, objects)

    def produce_profile(self, objects: List[ArtifactWrapper]) -> dict:
        """
        Wrapper for plugins parsing methods.
        """
        return self.produce_log(self.pro, objects)

    def produce_log(self, 
                    plugins: Any,
                    objects: List[ArtifactWrapper]) -> dict:
        """
        Wrapper for plugins parsing methods.
        """
        log = {
            "reports": [],
            "result": "valid"
        }
        for obj in objects:
            for lib in plugins:
                if lib == obj.library:
                    result = plugins[lib].render_datajudge(obj.result, obj.res_name)
                    log["reports"].append(result.to_dict())
            if obj.outcome == "invalid":
                log["result"] = "invalid"
        return log

    def render_schema(self,
                      schema: Any
                    ) -> list:
        """
        Render a list of schemas to be persisted.
        """
        return self.render_objects(schema, self.inf)
    
    def render_report(self,
                      report: Any
                      ) -> list:
        """
        Render a list of reports to be persisted.
        """
        return self.render_objects(report, self.val)

    def render_profile(self,
                       profile: Any
                       ) -> list:
        """
        Render a list of profiles to be persisted.
        """
        return self.render_objects(profile, self.pro)

    def render_objects(self,
                       objects: List[ArtifactWrapper],
                       plugin: Any
                       ) -> list:
        """
        Render a list of objects to be persisted.
        """
        if not isinstance(objects, list):
            objects = [objects]
        artifacts = []
        for obj in objects:
            lib = obj.library
            artifact = obj.result
            lib_plugin = plugin.get(lib)
            artifacts.extend(lib_plugin.render_artifact(artifact))
        return artifacts

    def get_info(self) -> dict:
        return {
            "validation": [self.val[lib].libraries() for lib in self.val],
            "inference": [self.inf[lib].libraries() for lib in self.inf],
            "profiling": [self.pro[lib].libraries() for lib in self.pro],
        }

    @property
    def inf(self) -> Any:
        return self._inference_plugins

    @property
    def val(self) -> Any:
        return self._validation_plugins

    @property
    def pro(self) -> Any:
        return self._profiling_plugins
