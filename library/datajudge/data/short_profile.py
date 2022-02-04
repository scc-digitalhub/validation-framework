"""
ShortProfile module.
Implementation of a Short Profile common structure.
"""

from collections import namedtuple


ProfileTuple = namedtuple("ProfileTuple",
                         ("duration", "stats", "fields"))


class ShortProfile:
    """
    ShortProfile object consisting in a succint
    version of an inferred data profile produced
    by some profiling framework.

    Attributes
    ----------
    lib_name : str
        Profiling library name.
    lib_version : str
        Profiling library version.
    data_resource_uri : str
        URI that point to the resource.
    duration : float
        Time required by the profiling process.
    stats : dict
        Descriptors of data stats.
    fields : dict
        Descriptors of data fields.

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
                 stats: dict,
                 fields: dict,
                 ) -> None:
        self.lib_name = lib_name
        self.lib_version = lib_version
        self.data_resource_uri = data_resource_uri
        self.duration = duration
        self.stats = stats
        self.fields = fields

    def to_dict(self) -> dict:
        """
        Return a dictionary of inferred schema.
        """
        schema = {
            "libraryName": self.lib_name,
            "libraryVersion": self.lib_version,
            "dataResourceUri": self.data_resource_uri,
            "duration": self.duration,
            "stats": self.stats,
            "fields": self.fields,
        }

        return schema

    def __repr__(self) -> str:
        return str(self.to_dict())
