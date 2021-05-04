"""
ShortSchema module.
Implementation of a Short Schema common structure.
"""
from collections import namedtuple
from typing import List


SchemaTuple = namedtuple("SchemaTuple", ("name", "type"))


class ShortSchema:
    """
    ShortSchema object consisting in a succint
    version of an inferred data schema produced
    by some validation framework.

    Attributes
    ----------
    fields : list
        A list of SchemaTuples with values 'name' & 'type'

    Methods
    -------
    to_dict :
        Return a dictionary schema.
    """
    def __init__(self, fields: List[SchemaTuple]) -> None:
        self._validate_fields(fields)
        self.fields = fields

    @staticmethod
    def _validate_fields(fields: List[SchemaTuple]) -> None:
        """
        Check if a non empty field list is made by
        SchemaTuples. If not, raise error.
        """
        for field in fields:
            if not isinstance(field, SchemaTuple):
                raise TypeError("Not a SchemaTuple!")

    def to_dict(self) -> dict:
        """
        Return a dictionary of inferred schema.
        """
        schema = {"fields": []}
        for field in self.fields:
            data = {"name": field.name,
                    "type": field.type}
            schema["fields"].append(data)
        return schema

    def __repr__(self) -> str:
        return str(self.to_dict())
