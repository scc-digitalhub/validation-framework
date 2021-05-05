"""
ShortReport module.
Implementation of a Short Report common structure.
"""
from datetime import datetime
from collections import namedtuple
from typing import Optional


ReportTuple = namedtuple("ReportTuple", ("time", "valid", "errors"))


class ShortReport:
    """
    Short report object consisting in a partial version of
    the full report produced by the validation library.

    Attributes
    ----------
    data_resource : str
        URI that point to the resource.
    experiment_name : str
        Name of the experiment.
    run_id : str
        Run id.
    time : datetime, default = None
        Time required by the validation process.
        Derived from the validation report.
    valid : bool, default = None
        Validation result.
        Derived from the validation report.
    errors : list, default = None
        List of errors found by validation process.
        Derived from the validation report.

    Methods
    -------
    to_dict :
        Transform the object in a dictionary.

    """

    def __init__(self,
                 data_resource: str,
                 experiment_name: str,
                 run_id: str,
                 time: Optional[datetime] = None,
                 valid: Optional[bool] = None,
                 errors: Optional[list] = None) -> None:
        self.data_resource = data_resource
        self.experiment_name = experiment_name
        self.run_id = run_id
        self.time = time
        self.valid = valid
        self.errors = errors

    def to_dict(self) -> dict:
        """
        Return a dictionary of the attributes.
        """
        return self.__dict__

    def __repr__(self) -> str:
        return str(self.__dict__)
