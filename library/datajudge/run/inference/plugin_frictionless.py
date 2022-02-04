"""
InferencePluginFrictionless module.
Implementation of a Run plugin that uses Frictionless as
inference framework.
"""
from __future__ import annotations

import typing
from typing import Optional

try:
    import frictionless
    from frictionless import Resource, describe_schema
    from frictionless.schema import Schema
except ImportError as ierr:
    raise ImportError("Please install frictionless!") from ierr

from datajudge.data import SchemaTuple
from datajudge.run.inference.inference_plugin import Inference
from datajudge.utils.utils import guess_mediatype, timer, warn

if typing.TYPE_CHECKING:
    from datajudge.data import DataResource


class InferencePluginFrictionless(Inference):
    """
    Frictionless inference plugin.
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
                     schema_inferred: Schema,
                     schema_path: Optional[str] = None
                     ) -> list:
        """
        Parse an inferred schema and return a field list for
        standardized ShortSchema.
        The process involves two steps:

            1. Retrieve the user validation schema if available.
            2. Parse the inferred schema and extract some
               infos from the user validation schema.

        The ShortSchema field description report the
        following informations:

            A. Name of the field
            B. Inferred type
            C. Expected type (from val. schema)
            D. Description (from val. schema)

        """

        # Can be empty dict!
        schema_valid = Schema(descriptor=schema_path)

        field_valid = schema_valid.get("fields", [])
        field_infer = schema_inferred.get("fields", [])
        short_schema_fields = []

        for fi in field_infer:

            fname = fi.get("name", "")
            ftype = fi.get("type", "")
            exp_type = ""
            desc = ""

            for fv in field_valid:
                if fname == fv.get("name"):
                    exp_type = fv.get("type", "")
                    desc = fv.get("description", "")
                    break

            schm_tpl = SchemaTuple(fname, ftype, exp_type, desc)
            short_schema_fields.append(schm_tpl)

        return short_schema_fields

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
