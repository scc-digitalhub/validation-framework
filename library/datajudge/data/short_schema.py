"""
ShortSchema module.
Implementation of a Short Schema common structure.
"""
from collections import namedtuple
from typing import List


class ShortSchema:
    """
    ShortSchema object consisting in a succint
    version of an inferred data schema produced
    by some validation framework.

    Attributes
    ----------
    lib_name : str
        Validation library name.
    lib_version : str
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
                 lib_name: str,
                 lib_version: str,
                 data_resource_uri: str,
                 duration: float,
                 fields: List[namedtuple]) -> None:
        self.lib_name = lib_name
        self.lib_version = lib_version
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
                "type": field.type
            }
            fields.append(data)

        schema = {
            "libraryName": self.lib_name,
            "libraryVersion": self.lib_version,
            "dataResourceUri": self.data_resource_uri,
            "duration": self.duration,
            "fields": fields,
        }

        return schema

    def __repr__(self) -> str:
        return str(self.to_dict())
