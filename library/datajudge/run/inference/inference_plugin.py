"""
Inference plugin abstract class module.
"""
# pylint: disable=import-error,invalid-name
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from typing import Any, List, Optional

from datajudge.run.results_registry import ResultsRegistry

SchemaTuple = namedtuple("SchemaTuple", ("name", "type"))
RenderTuple = namedtuple("RenderTuple", ("object", "filename"))


class Inference(metaclass=ABCMeta):
    """
    Run plugin that executes inference over a Resource.
    """

    def __init__(self) -> None:
        self.lib_name = None
        self.lib_version = None
        self.registry = ResultsRegistry()
        self.update_library_info()

    @abstractmethod
    def update_library_info(self) -> None:
        """
        Update metadata about the validation framework used.
        """

    @abstractmethod
    def parse_schema(self,
                     schema_inferred: Any
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
    def infer(self,
              res_name: str,
              data_path: str) -> Any:
        """
        Inference method for schema.
        """

    @abstractmethod
    def render_object(self, obj: Any) -> List[RenderTuple]:
        """
        Return a rendered schema ready to be persisted as artifact.
        """
