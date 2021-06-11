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
                 data_resource_uri: str,
                 duration: float,
                 stats: dict,
                 fields: dict,
                 ) -> None:
        self.data_resource_uri = data_resource_uri
        self.duration = duration
        self.stats = stats
        self.fields = fields

    def to_dict(self) -> dict:
        """
        Return a dictionary of inferred schema.
        """
        schema = {
            "data_resource_uri": self.data_resource_uri,
            "duration": self.duration,
            "stats": self.stats,
            "fields": self.fields,
        }

        return schema

    def __repr__(self) -> str:
        return str(self.to_dict())
