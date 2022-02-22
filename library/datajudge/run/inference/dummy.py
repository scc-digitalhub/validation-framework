"""
Dummy implementation of inference plugin.
"""
from typing import Any, List

from datajudge.run.inference.inference_plugin import (Inference, RenderTuple,
                                                      SchemaTuple)


FN_SCHEMA = "schema_dummy.json"


class InferencePluginDummy(Inference):
    """
    Dummy implementation of inference plugin.
    """

    def update_library_info(self) -> None:
        """
        Update run's info about the inference framework used.
        """
        self.lib_name = None
        self.lib_version = None

    def parse_schema(self,
                     schema_inferred: Any
                     ) -> list:
        """
        Return empty schema tuple.
        """
        return [SchemaTuple("", "")]

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
        self.registry.add_result(res_name, inferred, None)

        return inferred

    def render_object(self, obj: Any) -> List[RenderTuple]:
        """
        Return a dummy profile to be persisted as artifact.
        """
        return [RenderTuple({}, FN_SCHEMA)]
