"""
Run plugins registry module.
"""
from __future__ import annotations

import typing
from typing import Any

from datajudge.run.plugin.plugin_factory import get_plugin

if typing.TYPE_CHECKING:
    from datajudge import RunConfig


class PluginHandler:
    
    def __init__(self, run_config: RunConfig) -> None:

        self._inference_plugins = get_plugin(run_config.inference,
                                             "inference")
        self._validation_plugins = get_plugin(run_config.validation,
                                      "validation")
        self._profiling_plugins = get_plugin(run_config.profiling,
                                      "profiling")

    def infer(self, *args, **kwargs) -> Any:
        return self.execute(self.inf, *args, **kwargs)

    def validate(self, *args, **kwargs) -> Any:
        return self.execute(self.val, *args, **kwargs)
    
    def profile(self, *args, **kwargs) -> Any:
        return self.execute(self.pro, *args, **kwargs)

    def execute(self, plugin, *args, **kwargs) -> Any:
        results = []
        for lib in plugin:
            result = plugin[lib].execute(*args, **kwargs)
            results.append({
                "library": plugin[lib].lib_name,
                "result": result
            })
        return results

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
                       objects: Any,
                       plugin: Any
                       ) -> list:
        """
        Render a list of objects to be persisted.
        """
        if not isinstance(objects, list):
            objects = [objects]
        artifacts = []
        for obj in objects:
            lib = obj.get("library")
            artifact = obj.get("result")
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
