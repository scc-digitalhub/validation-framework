"""
Frictionless implementation of inference plugin.
"""
from __future__ import annotations

import time
import typing
from typing import List, Optional

import frictionless
from frictionless import Resource, describe_schema
from frictionless.schema import Schema

import datajudge.utils.config as cfg
from datajudge.run.inference.inference_plugin import (Inference, RenderTuple,
                                                      SchemaTuple)
from datajudge.utils.utils import guess_mediatype, warn

if typing.TYPE_CHECKING:
    from datajudge.data import DataResource


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

    def update_data_resource(self,
                             resource: DataResource,
                             data_path: str) -> None:
        """
        Update resource with inferred information.
        """
        inferred = self.infer_resource(data_path)

        # Profile, format, encoding
        for key in ["profile", "format", "encoding"]:
            value = inferred.get(key)
            setattr(resource, key, value)

        # Bytes, MD5 Hash
        for key in ["bytes", "hash"]:
            value = inferred.get("stats", {}).get(key)
            setattr(resource, key, value)

        # Mediatype
        mediatype = guess_mediatype(resource.path)
        setattr(resource, "mediatype", mediatype)

    def parse_schema(self,
                     schema_inferred: Schema
                     ) -> list:
        """
        Parse an inferred schema and return a field list for
        standardized DatajudgeSchema.
        """

        field_infer = schema_inferred.get("fields", [])
        dj_schema_fields = []

        for fi in field_infer:
            fname = fi.get("name", "")
            ftype = fi.get("type", "")
            dj_schema_fields.append(SchemaTuple(fname, ftype))
        if dj_schema_fields:
            return dj_schema_fields
        return [SchemaTuple("", "")]

    def validate_schema(self, schema: Schema) -> None:
        """
        Validate frictionless schema before persist it.
        """
        if not isinstance(schema, Schema):
            raise TypeError("Expected frictionless schema!")

    def infer(self,
              res_name: str,
              data_path: str) -> Schema:
        """
        Method that call infer on a resource and return an
        inferred schema.
        """
        inferred = self.registry.get_result(res_name)
        if inferred is not None:
            return inferred

        # Execute inference and measure time
        start = time.perf_counter()
        inferred = describe_schema(data_path)
        end = round(time.perf_counter() - start, 2)

        if inferred is None:
            warn("Unable to infer schema.")
            return

        self.registry.add_result(res_name, inferred, end)

        return inferred

    def infer_resource(self, data_path: str) -> Resource:
        """
        Infer on resource.
        """
        resource = Resource(path=data_path)
        resource.infer(stats=True)
        resource.expand()
        return resource

    def render_object(self, obj: Schema) -> List[RenderTuple]:
        """
        Return a rendered profile ready to be persisted as artifact.
        """

        self.validate_schema(obj)
        dict_schema = dict(obj)

        return [RenderTuple(dict_schema, cfg.FN_INFERRED_SCHEMA)]
