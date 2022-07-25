"""
Datajudge base report module.
"""
from abc import ABCMeta
from dataclasses import dataclass


@dataclass
class DatajudgeBaseReport(metaclass=ABCMeta):
    """
    Datajudge base report abstract class.

    Attributes
    ----------
    lib_name : str
        Execution library name.
    lib_version : str
        Execution library version.
    duration : float
        Time required by the execution process.

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
    Succint version of a profile produced by some profiling library.

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
    Succint version of a report produced by some validation library.

    Attributes
    ----------
    constraint : dict
        Constraint validated.
    valid : bool
        Validation outcome.
    errors : list
        List of errors found by validation process.

    """
    constraint: dict
    valid: bool
    errors: list


@dataclass
class DatajudgeSchema(DatajudgeBaseReport):
    """
    Succint version of an inferred schema produced by some inference library.

    Attributes
    ----------
    fields : list
        A list of fields.

    """
    fields: list
