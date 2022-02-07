"""
ShortReport module.
Implementation of a Short Report common structure.
"""
# pylint: disable=too-many-arguments
from typing import List, Mapping


class ShortReport:
    """
    Short report object consisting in a partial version of
    the full report produced by the validation library.

    Attributes
    ----------
    lib_name : str
        Validation library name.
    lib_version : str
        Validation library version.
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
                 lib_name: str,
                 lib_version: str,
                 data_resource_uri: str,
                 duration: float,
                 valid: bool,
                 errors: List[Mapping]) -> None:
        self.lib_name = lib_name
        self.lib_version = lib_version
        self.data_resource_uri = data_resource_uri
        self.duration = duration
        self.valid = valid
        self.errors = errors

    def to_dict(self) -> dict:
        """
        Return a dictionary of the attributes.
        """
        report = {
            "libraryName": self.lib_name,
            "libraryVersion": self.lib_version,
            "dataResourceUri": self.data_resource_uri,
            "duration": self.duration,
            "valid": self.valid,
            "errors": self.errors,
        }
        return report

    def __repr__(self) -> str:
        return str(self.to_dict())
