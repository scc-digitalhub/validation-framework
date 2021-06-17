"""
ShortProfile module.
Implementation of a Short Profile common structure.
"""


class ShortProfile:
    """
    ShortProfile object consisting in a succint
    version of an inferred data profile produced
    by some profiling framework.

    Attributes
    ----------
    pro_lib_name : str
        Profiling library name.
    pro_lib_version : str
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
                 pro_lib_name: str,
                 pro_lib_version: str,
                 data_resource_uri: str,
                 duration: float,
                 stats: dict,
                 fields: dict,
                 ) -> None:
        self.pro_lib_name = pro_lib_name
        self.pro_lib_version = pro_lib_version
        self.data_resource_uri = data_resource_uri
        self.duration = duration
        self.stats = stats
        self.fields = fields

    def to_dict(self) -> dict:
        """
        Return a dictionary of inferred schema.
        """
        schema = {
            "profiling_library_name": self.pro_lib_name,
            "profiling_library_version": self.pro_lib_version,
            "data_resource_uri": self.data_resource_uri,
            "duration": self.duration,
            "stats": self.stats,
            "fields": self.fields,
        }

        return schema

    def __repr__(self) -> str:
        return str(self.to_dict())
