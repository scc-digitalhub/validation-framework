"""
DatajudgeSchema module.
Implementation of a Short Schema common structure.
"""
# pylint: disable=too-many-arguments,too-few-public-methods
from typing import Union
from datajudge.data.datajudge_base_report import DatajudgeBaseReport


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
    def __init__(self,
                 lib_name: str,
                 lib_version: str,
                 duration: float,
                 fields: list) -> None:
        super().__init__(lib_name, lib_version, duration)
        self.fields = fields

    def to_dict(self) -> dict:
        """
        Return a dictionary of inferred schema.
        """
        schema = {
            "libraryName": self.lib_name,
            "libraryVersion": self.lib_version,
            "duration": self.duration,
            "fields": self.fields,
        }
        return schema
