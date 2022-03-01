"""
Run plugins handler module.
"""
from dataclasses import dataclass
from typing import Any, List


@dataclass
class ArtifactWrapper:
    """
    Simple mapper for artifacts.
    """
    res_name: str
    library: str
    result: Any
    outcome: str


class PluginHandler:
    """
    Run plugin handler.

    This class create a layer of abstraction between the Run
    and its plugins.
    This allows to wrap the plagin methods and run operation
    before or after the actual execution.

    """

    def __init__(self,
                 inference_plugin: Any,
                 validation_plugin: Any,
                 profiling_plugin: Any) -> None:
        self._inference_plugins = inference_plugin
        self._validation_plugins = validation_plugin
        self._profiling_plugins = profiling_plugin

    def infer(self,
              res_name: str,
              data_path: str,
              exec_args: dict,
              *args, **kwargs) -> List[ArtifactWrapper]:
        """
        Wrapper for plugins infer methods.
        """
        return self.get_cached_results(self.inf,
                                       res_name,
                                       data_path,
                                       exec_args,
                                       *args, **kwargs)

    def validate(self,
                 res_name: str,
                 data_path: str,
                 constraints: list,
                 exec_args: dict,
                 *args, **kwargs) -> List[ArtifactWrapper]:
        """
        Wrapper for plugins validate methods.
        """
        const_type = {}

        # Loop through constraints and extract 
        # resources and constraints for a specific plugin.
        for constraint in constraints:
            if constraint.type not in const_type:
                const_type[constraint.type] = {
                                        "res": [],
                                        "const": []
                                    }
            const_type[constraint.type]["const"].append(constraint)
            const_type[constraint.type]["res"].extend(constraint.resources)

        # Plugin rebuild constraints and register resources
        # needed by validation and constraints related.
        for library, values in const_type.items():
            for plugin in self.val:
                if library == self.val[plugin].lib_name:
                    [self.val[plugin].registry.register_resource(res)
                     for res in  values["res"]]
                    self.val[plugin].rebuild_constraint(values["const"])

        return self.get_cached_results(self.val,
                                       res_name,
                                       data_path,
                                       exec_args,
                                       *args, **kwargs)

    def profile(self, 
                res_name: str,
                data_path: str,
                exec_args: dict,
                *args, **kwargs) -> List[ArtifactWrapper]:
        """
        Wrapper for plugins profile methods.
        """
        return self.get_cached_results(self.pro,
                                       res_name,
                                       data_path,
                                       exec_args,
                                       *args, **kwargs)

    def get_cached_results(self, 
                           plugin: Any,
                           res_name: str,
                           data_path: str,
                           exec_args: dict,
                           *args, **kwargs) -> Any:
        
        # Loop over plugin registry registry and try to fetch
        # cached results.
        results = []
        for lib in plugin:
            result = plugin[lib].registry.get_result(res_name)
            if result is not None:
                outcome = plugin[lib].registry.get_outcome(res_name)
                results.append(ArtifactWrapper(res_name,
                                               lib,
                                               result,
                                               outcome))

        if len(results) != len(plugin):
            return self.execute(plugin,
                                res_name,
                                data_path,
                                exec_args,
                                *args, **kwargs)
        return results
    
    @staticmethod
    def execute(plugin: Any,
                res_name: str,
                data_path: str,
                exec_args: dict,
                *args, **kwargs) -> List[ArtifactWrapper]:
        """
        Wrap plugin main execution method.
        """
        if exec_args is None:
            exec_args = {}

        results = []
        for lib in plugin:
            plugin[lib].registry.register_resource(res_name)
            result = plugin[lib].execute(res_name,
                                         data_path,
                                         exec_args.get(lib, {}),
                                         *args,
                                         **kwargs)
            outcome = plugin[lib].registry.get_outcome(res_name)
            results.append(ArtifactWrapper(res_name, lib, result, outcome))
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

    @staticmethod
    def produce_log(plugins: Any,
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
                    result = plugins[lib].render_datajudge(obj.result,
                                                           obj.res_name)
                    log["reports"].append(result.to_dict())
            if obj.outcome == "invalid":
                log["result"] = "invalid"

        if len(log["reports"]) != len(plugins):
            log["result"] = "invalid"

        return log

    def render_schema(self, schema: Any) -> list:
        """
        Render a list of schemas to be persisted.
        """
        return self.render_objects(schema, self.inf)

    def render_report(self, report: Any) -> list:
        """
        Render a list of reports to be persisted.
        """
        return self.render_objects(report, self.val)

    def render_profile(self, profile: Any) -> list:
        """
        Render a list of profiles to be persisted.
        """
        return self.render_objects(profile, self.pro)

    @staticmethod
    def render_objects(objects: List[ArtifactWrapper],
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
        """
        Return libraries of plugins.
        """
        return {
            "validation": [self.val[lib].libraries() for lib in self.val],
            "inference": [self.inf[lib].libraries() for lib in self.inf],
            "profiling": [self.pro[lib].libraries() for lib in self.pro],
        }

    @property
    def inf(self) -> Any:
        """
        Inference plugin getter.
        """
        return self._inference_plugins

    @property
    def val(self) -> Any:
        """
        Validation plugin getter.
        """
        return self._validation_plugins

    @property
    def pro(self) -> Any:
        """
        Profiling plugin getter.
        """
        return self._profiling_plugins
