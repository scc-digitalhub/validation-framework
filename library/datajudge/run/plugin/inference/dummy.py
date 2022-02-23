"""
Dummy implementation of inference plugin.
"""
from typing import Any, List

from datajudge.run.plugin.inference.inference_plugin import Inference


class InferencePluginDummy(Inference):
    """
    Dummy implementation of inference plugin.
    """

    def update_library_info(self) -> None:
        """
        Do nothing.
        """

    def parse_schema(self,
                     schema_inferred: Any
                     ) -> list:
        """
        Return empty schema tuple.
        """
        return [self.get_schema_tuple(None, None)]

    def validate_schema(self, schema: Any) -> None:
        """
        Do nothing.
        """

    def infer(self,
              res_name: str,
              data_path: str) -> Any:
        """
        Method that call infer on a resource and return an
        inferred schema.
        """
        inferred = self.registry.get_result(res_name)
        if inferred is not None:
            return inferred
        inferred = {}
        self.registry.add_result(res_name, inferred)
        return inferred

    def render_artifact(self, obj: Any) -> List[tuple]:
        """
        Return a dummy profile to be persisted as artifact.
        """
        schema = dict()
        filename = self._fn_schema.format("dummy.json")
        return [self.get_render_tuple(schema, filename)]
