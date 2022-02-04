"""
RunInference class module.
The RunInference class describes a Run object that performs
inference tasks over a Resource. With inference task, we mean
a general description of a resource (extension, metadata etc.)
and the inference of a data schema (field types).
"""

# pylint: disable=import-error,invalid-name
from __future__ import annotations
from collections import namedtuple

import typing
from abc import ABCMeta, abstractmethod
from typing import Any

if typing.TYPE_CHECKING:
    from datajudge.client import Client
    from datajudge.data import DataResource
    from datajudge.run import RunInfo


class Validation(object, metaclass=ABCMeta):
    """
    Run plugin that executes validation over a Resource.
    """
   
    def __init__(self) -> None:

        self.lib_name = None
        self.lib_version = None
        self.update_library_info()

    @abstractmethod
    def update_library_info(self) -> None:
        """
        Update run's info about the validation framework used.
        """

    @abstractmethod
    def parse_report(self,
                      nmtp: namedtuple) -> namedtuple:
        """
        Parse the report produced by the validation framework.
        """

    @abstractmethod
    def validate_report(self,
                      report: Any) -> None:
        """
        Check a report before log/persist it.
        """

    @abstractmethod
    def validate(self) -> None:
        pass
