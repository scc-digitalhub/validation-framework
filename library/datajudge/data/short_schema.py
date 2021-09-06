"""
ShortSchema module.
Implementation of a Short Schema common structure.
"""
from collections import namedtuple
from typing import List


SchemaTuple = namedtuple("SchemaTuple", ("name", "type",
                                         "valid_type", "description"))


class ShortSchema:
    """
    ShortSchema object consisting in a succint
    version of an inferred data schema produced
    by some validation framework.

    Attributes
    ----------
    val_lib_name : str
        Validation library name.
    val_lib_version : str
        Validation library version.
    data_resource_uri : str
        URI that point to the resource.
    duration : float
        Time required by the inference process.
    fields : list
        A list of SchemaTuples with values 'name' & 'type'.

    Methods
    -------
    to_dict :
        Return a dictionary schema.
    """
    def __init__(self,
                 val_lib_name: str,
                 val_lib_version: str,
                 data_resource_uri: str,
                 duration: float,
                 fields: List[SchemaTuple]) -> None:
        self.val_lib_name = val_lib_name
        self.val_lib_version = val_lib_version
        self.data_resource_uri = data_resource_uri
        self.duration = duration
        self.fields = fields

    def to_dict(self) -> dict:
        """
        Return a dictionary of inferred schema.
        """
        fields = []
        for field in self.fields:
            data = {
                "name": field.name,
                "type": field.type,
                "validType": field.valid_type,
                "description": field.description
            }
            fields.append(data)

        schema = {
            "validationLibraryName": self.val_lib_name,
            "validationLibraryVersion": self.val_lib_version,
            "data_resource_uri": self.data_resource_uri,
            "duration": self.duration,
            "fields": fields,
        }

        return schema

    def __repr__(self) -> str:
        return str(self.to_dict())
