"""
Datajudge base report module.
"""
# pylint: disable=too-many-arguments,too-few-public-methods
from abc import ABCMeta
from dataclasses import dataclass


@dataclass
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
    to_dict :
        Return a dictionary report.

    """

    lib_name: str
    lib_version: str
    duration: float

    def to_dict(self) -> dict:
        """
        Return a dictionary of the instance.
        """
        return self.__dict__

    def __repr__(self) -> str:
        return str(self.to_dict())


@dataclass
class DatajudgeProfile(DatajudgeBaseReport):
    """
    DatajudgeProfile object consisting in a succint
    version of an inferred data profile produced by
    some profiling framework.

    Attributes
    ----------
    stats : dict
        Descriptors of data stats.
    fields : dict
        Descriptors of data fields.

    """
    stats: dict
    fields: dict


@dataclass
class DatajudgeReport(DatajudgeBaseReport):
    """
    Short report object consisting in a succint
    version of a report produced by some validation
    library.

    Attributes
    ----------
    valid : bool
        Validation outcome.
        Derived from the validation report.
    errors : list
        List of errors found by validation process.
        Derived from the validation report.

    """
    constraint: dict
    valid: bool
    errors: list


@dataclass
class DatajudgeSchema(DatajudgeBaseReport):
    """
    DatajudgeSchema object consisting in a succint
    version of an inferred data schema produced
    by some validation framework.

    Attributes
    ----------
    fields : list
        A list of fields.

    """
    fields: list
