"""
Dummy implementation of inference plugin.
"""
from typing import Any, List, Optional

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
              data_path: str,
              infer_kwargs: Optional[dict] = None) -> Any:
        """
        Generate dummy schema.
        """
        return {}

    def render_artifact(self, obj: Any) -> List[tuple]:
        """
        Return a dummy schema to be persisted as artifact.
        """
        schema = {}
        filename = self._fn_schema.format("dummy.json")
        return [self.get_render_tuple(schema, filename)]
