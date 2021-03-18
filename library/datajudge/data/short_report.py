from datetime import datetime
from typing import Optional


class ShortReport:
    """Short report object."""
    
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