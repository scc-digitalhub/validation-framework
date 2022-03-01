"""
Inference plugin abstract class module.
"""
# pylint: disable=import-error,invalid-name
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from typing import Any, Optional

from datajudge.data import DatajudgeSchema
from datajudge.run.plugin.base_plugin import Plugin


SchemaTuple = namedtuple("SchemaTuple", ("name", "type"))


class Inference(Plugin, metaclass=ABCMeta):
    """
    Run plugin that executes inference over a Resource.
    """

    _fn_schema = "schema_{}"

    @abstractmethod
    def parse_schema(self,
                     schema_inferred: Any
                     ) -> list:
        """
        Parse the inferred schema produced by the validation
        framework.
        """

    @abstractmethod
    def validate_schema(self, schema: Any) -> None:
        """
        Validate a schema before log/persist it.
        """

    @abstractmethod
    def infer(self,
              res_name: str,
              data_path: str,
              exec_args: dict) -> Any:
        """
        Inference method for schema.
        """

    def execute(self, *args, **kwargs) -> Any:
        """
        Execute plugin main operation.
        """
        return self.infer(*args, **kwargs)

    def render_datajudge(self,
                         schema: Any,
                         res_name: str) -> DatajudgeSchema:
        """
        Return a DatajudgeSchema.
        """
        parsed = self.parse_schema(schema)
        return DatajudgeSchema(self.lib_name,
                               self.lib_version,
                               self.registry.get_time(res_name),
                               parsed)

    @staticmethod
    def get_schema_tuple(name: str,
                         type_: str) -> SchemaTuple:
        """
        Return SchemaTuple.
        """
        return SchemaTuple(name, type_)
