"""
RunInference class module.
The RunInference class describes a Run object that performs
inference tasks over a Resource. With inference task, we mean
a general description of a resource (extension, metadata etc.)
and the inference of a data schema (field types).
"""

# pylint: disable=import-error,invalid-name
from __future__ import annotations

import typing
from abc import ABCMeta, abstractmethod
from typing import Any, Optional

if typing.TYPE_CHECKING:
    from datajudge.client import Client
    from datajudge.data import DataResource


class Inference(object, metaclass=ABCMeta):
    """
    Run plugin that executes inference over a Resource.
    """

    def __init__(self) -> None:

        self.lib_name = None
        self.lib_version = None
        self.update_library_info()

    @abstractmethod
    def update_library_info(self) -> None:
        """
        Update metadata about the validation framework used.
        """

    @abstractmethod
    def update_data_resource(self,
                             resource: DataResource,
                             data_path: str) -> None:
        """
        Update resource with inferred information.
        """

    @abstractmethod
    def parse_schema(self,
                     client: Client,
                     schema_inferred: Any,
                     schema_uri: Optional[str] = None
                     ) -> list:
        """
        Parse the inferred schema produced by the validation
        framework.
        """

    @abstractmethod
    def validate_schema(self,
                        schema: Any) -> None:
        """
        Validate a schema before log/persist it.
        """

    @abstractmethod
    def infer_schema(self) -> Any:
        """
        Inference method for schema.
        """

    @abstractmethod
    def infer_resource(self) -> Any:
        """
        Inference method for resource.
        """
