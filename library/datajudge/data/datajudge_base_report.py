"""
Datajudge base report module.
"""
# pylint: disable=too-many-arguments,too-few-public-methods
from abc import ABCMeta, abstractmethod


class DatajudgeBaseReport(metaclass=ABCMeta):
    """
    Datajudge base report abstract class

    Attributes
    ----------
    lib_name : str
        Execution library name.
    lib_version : str
        Execution library version.
    duration : float
        Time required by the execution process.

    Methods
    -------
    dict :
        Return a dictionary schema.

    """

    def __init__(self,
                 lib_name: str,
                 lib_version: str,
                 duration: float
                 ) -> None:
        self.lib_name = lib_name
        self.lib_version = lib_version
        self.duration = duration

    @abstractmethod
    def to_dict(self) -> dict:
        """
        Return a dictionary of the instance.
        """

    def __repr__(self) -> str:
        return str(self.to_dict())
