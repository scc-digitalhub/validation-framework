"""
Inference plugin abstract class module.
"""
# pylint: disable=import-error,invalid-name
from __future__ import annotations
from collections import namedtuple

import typing
from abc import ABCMeta, abstractmethod
from typing import Any, List, Optional

if typing.TYPE_CHECKING:
    from datajudge.data import DataResource

SchemaTuple = namedtuple("SchemaTuple", ("name", "type",
                                         "valid_type", "description"))
RenderTuple = namedtuple("RenderTuple",
                         ("object", "filename"))


class Inference(metaclass=ABCMeta):
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
                     schema_inferred: Any,
                     schema_path: Optional[str] = None
                     ) -> list:
        """
        Parse the inferred schema produced by the validation
        framework.
        """

    @abstractmethod
    def validate_schema(self,
                        schema: Optional[Any] = None
                        ) -> None:
        """
        Validate a schema before log/persist it.
        """

    @abstractmethod
    def infer_schema(self,
                     data_path: str) -> Any:
        """
        Inference method for schema.
        """

    @abstractmethod
    def infer_resource(self,
                       data_path: str) -> Any:
        """
        Inference method for resource.
        """

    @abstractmethod
    def render_object(self,
                      obj: Any) -> List[RenderTuple]:
        """
        Return a rendered schema ready to be persisted as artifact.
        """
