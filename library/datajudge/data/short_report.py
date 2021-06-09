"""
ShortReport module.
Implementation of a Short Report common structure.
"""
from collections import namedtuple
from typing import Optional


# pylint: disable=too-many-arguments

ReportTuple = namedtuple("ReportTuple", ("time", "valid", "errors"))


class ShortReport:
    """
    Short report object consisting in a partial version of
    the full report produced by the validation library.

    Attributes
    ----------
    data_resource_uri : str
        URI that point to the resource.
    duration : float
        Time required by the validation process.
        Derived from the validation report.
    valid : bool
        Validation outcome.
        Derived from the validation report.
    errors : list
        List of errors found by validation process.
        Derived from the validation report.

    Methods
    -------
    to_dict :
        Transform the object in a dictionary.

    """

    def __init__(self,
                 data_resource_uri: str,
                 duration: float,
                 valid: bool,
                 errors: list) -> None:
        self.data_resource_uri = data_resource_uri
        self.duration = duration
        self.valid = valid
        self.errors = errors

    def to_dict(self) -> dict:
        """
        Return a dictionary of the attributes.
        """
        report = {
            "data_resource_uri": self.data_resource_uri,
            "duration": self.duration,
            "valid": self.valid,
            "errors": self.errors,
        }
        return report

    def __repr__(self) -> str:
        return str(self.to_dict())
