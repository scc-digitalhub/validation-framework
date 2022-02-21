"""
Frictionless implementation of inference plugin.
"""
from __future__ import annotations

import typing
from typing import List, Optional

import frictionless
from frictionless import Resource, describe_schema
from frictionless.schema import Schema

import datajudge.utils.config as cfg
from datajudge.run.inference.inference_plugin import (Inference, RenderTuple,
                                                      SchemaTuple)
from datajudge.utils.utils import guess_mediatype, timer, warn

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
        standardized ShortSchema.
        """

        field_infer = schema_inferred.get("fields", [])
        short_schema_fields = []

        for fi in field_infer:
            fname = fi.get("name", "")
            ftype = fi.get("type", "")
            short_schema_fields.append(SchemaTuple(fname, ftype))
        if short_schema_fields:
            return short_schema_fields
        return [SchemaTuple("", "")]

    def validate_schema(self,
                        schema: Optional[Schema] = None) -> None:
        """
        Validate frictionless schema before log/persist it.
        """
        if schema is not None and not isinstance(schema, Schema):
            raise TypeError("Expected frictionless schema!")

    @timer
    def infer_schema(self,
                     data_path: str) -> Schema:
        """
        Method that call infer on a frictionless Resource
        and return an inferred schema.
        """
        schema = describe_schema(data_path)
        if schema is None:
            warn("Unable to infer schema.")
        return schema

    def infer_resource(self,
                       data_path: str) -> Resource:
        """
        Infer on resource.
        """
        resource = Resource(path=data_path)
        resource.infer(stats=True)
        resource.expand()
        return resource

    def render_object(self,
                      obj: Schema) -> List[RenderTuple]:
        """
        Return a rendered profile ready to be persisted as artifact.
        """

        self.validate_schema(obj)
        dict_schema = dict(obj)

        return [RenderTuple(dict_schema, cfg.FN_INFERRED_SCHEMA)]
