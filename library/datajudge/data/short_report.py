from datetime import datetime
from typing import Optional


class ShortReport:
    """Short report object.

    Attributes
    ----------
    data_resource :
        URI that point to the resource.
    experiment_name :
        Name of the experiment.
    run_id :
        Run id.
    time :
        Time required by the validation process.
        Derived from the validation report.
    valid :
        Validation result.
        Derived from the validation report.
    errors :
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

    def to_dict(self):
        """Return a dictionary of the attributes."""
        return self.__dict__

    def __repr__(self):
        return str(self.__dict__)