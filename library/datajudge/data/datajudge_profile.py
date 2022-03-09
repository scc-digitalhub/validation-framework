"""
DatajudgeProfile module.
Implementation of a Short Profile common structure.
"""
# pylint: disable=too-many-arguments
from datajudge.data.datajudge_base_report import DatajudgeBaseReport


class DatajudgeProfile(DatajudgeBaseReport):
    """
    DatajudgeProfile object consisting in a succint
    version of an inferred data profile produced
    by some profiling framework.

    Attributes
    ----------
    stats : dict
        Descriptors of data stats.
    fields : dict
        Descriptors of data fields.

    """
    def __init__(self,
                 lib_name: str,
                 lib_version: str,
                 duration: float,
                 stats: dict,
                 fields: dict) -> None:
        super().__init__(lib_name, lib_version, duration)
        self.stats = stats
        self.fields = fields

    def dict(self) -> dict:
        """
        Return a dictionary of inferred schema.
        """
        schema = {
            "libraryName": self.lib_name,
            "libraryVersion": self.lib_version,
            "duration": self.duration,
            "stats": self.stats,
            "fields": self.fields,
        }
        return schema
