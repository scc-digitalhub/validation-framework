"""
Inference plugin abstract class module.
"""
# pylint: disable=import-error,invalid-name
from __future__ import annotations

import time
import typing
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from typing import Any, List

from datajudge.data import DatajudgeSchema
from datajudge.run.plugin.base_plugin import Plugin

if typing.TYPE_CHECKING:
    from datajudge.run.plugin.base_plugin import Result


SchemaTuple = namedtuple("SchemaTuple", ("time", "fields"))


class Inference(Plugin, metaclass=ABCMeta):
    """
    Run plugin that executes inference over a Resource.
    """

    _fn_schema = "schema_{}"

    def execute(self) -> Result:
        """
        Method that call specific execution.
        """
        try:
            self.result.status = self._STATUS_RUNNING
            start = time.perf_counter()
            self.result.artifact = self.infer()
            self.result.time = round(time.perf_counter() - start, 2)
            self.result.status = self._STATUS_FINISHED
        except Exception:
            self.result.status = self._STATUS_ERROR

        return self.result

    @abstractmethod
    def infer(self) -> Any:
        """
        Inference method for schema.
        """

    @abstractmethod
    def produce_schema(self,
                       obj: Result) -> List[SchemaTuple]:
        """
        Produce datajudge schema by parsing framework
        results.
        """

    def render_datajudge(self,
                         obj: Result) -> DatajudgeSchema:
        """
        Return a DatajudgeSchema.
        """
        parsed = self.produce_schema(obj)
        return DatajudgeSchema(self.get_lib_name(),
                               self.get_lib_version(),
                               parsed.time,
                               parsed.fields)

    @staticmethod
    def get_schema_tuple(name: str,
                         type_: str) -> SchemaTuple:
        """
        Return SchemaTuple.
        """
        return SchemaTuple(name, type_)
