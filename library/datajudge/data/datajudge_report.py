"""
DatajudgeReport module.
Implementation of a Short Report common structure.
"""
# pylint: disable=too-many-arguments,too-few-public-methods
from typing import List, Mapping, Union

from datajudge.data.datajudge_base_report import DatajudgeBaseReport


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

    def __init__(self,
                 lib_name: str,
                 lib_version: str,
                 execution_errors: Union[str, list],
                 duration: float,
                 constraint: dict,
                 valid: bool,
                 errors: List[Mapping]) -> None:
        super().__init__(lib_name, lib_version, execution_errors, duration)
        self.constraint = constraint
        self.valid = valid
        self.errors = errors

    def to_dict(self) -> dict:
        """
        Return a dictionary of the attributes.
        """
        report = {
            "libraryName": self.lib_name,
            "libraryVersion": self.lib_version,
            "execution_errors": self.execution_errors,
            "duration": self.duration,
            "constraint": self.constraint,
            "valid": self.valid,
            "errors": self.errors,
        }
        return report
