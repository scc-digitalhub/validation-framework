"""
Frictionless implementation of inference plugin.
"""
# pylint: disable=import-error
import time
import warnings
from typing import List, Optional

import frictionless
from frictionless import describe_schema
from frictionless.schema import Schema

from datajudge.run.plugin.inference.inference_plugin import Inference


class InferencePluginFrictionless(Inference):
    """
    Frictionless implementation of inference plugin.
    """

    def update_library_info(self) -> None:
        """
        Update run's info about the inference framework used.
        """
        self.lib_name = frictionless.__name__
        self.lib_version = frictionless.__version__

    def parse_schema(self,
                     schema_inferred: Schema
                     ) -> list:
        """
        Parse an inferred schema and return a field list for
        standardized DatajudgeSchema.
        """

        field_infer = schema_inferred.get("fields", [])
        dj_schema_fields = []

        for field in field_infer:
            field_name = field.get("name", "")
            field_type = field.get("type", "")
            dj_schema_fields.append(self.get_schema_tuple(field_name,
                                                          field_type))
        if dj_schema_fields:
            return dj_schema_fields
        return [self.get_schema_tuple(None, None)]

    def validate_schema(self, schema: Schema) -> None:
        """
        Validate frictionless schema before persist it.
        """
        if not isinstance(schema, Schema):
            raise TypeError("Expected frictionless schema!")

    def infer(self,
              res_name: str,
              data_path: str,
              exec_args: dict) -> Schema:
        """
        Method that call infer on a resource and return an
        inferred schema.
        """
        # Execute inference and measure time
        start = time.perf_counter()
        inferred = describe_schema(data_path, **exec_args)
        end = round(time.perf_counter() - start, 2)

        result = self.get_outcome(inferred)

        self.registry.add_result(res_name, inferred, result, end)

        return inferred

    def get_outcome(self, obj: Schema) -> str:
        """
        Return status of the execution.
        """
        if obj is not None and obj != {}:
            return self._VALID_STATUS
        return self._INVALID_STATUS

    def render_artifact(self, obj: Schema) -> List[tuple]:
        """
        Return a rendered profile ready to be persisted as artifact.
        """
        self.validate_schema(obj)
        schema = dict(obj)
        filename = self._fn_schema.format("frictionless.json")
        return [self.get_render_tuple(schema, filename)]
