from collections import namedtuple
from typing import List


SchemaTuple = namedtuple("SchemaTuple", ("name", "type"))

class ShortSchema:
    def __init__(self, fields: List[SchemaTuple]) -> None:
        self._validate_fields(fields)
        self.fields = fields
        self.schema = {"fields": []}

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
        for field in self.fields:
            self.schema["fields"].append({
                    "name": field.name,
                    "type": field.type})
        return self.schema

    def __repr__(self) -> str:
        return str(self.to_dict())