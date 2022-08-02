"""
FileReader module.
"""
from typing import Optional
from datajudge.data_reader.base_data_reader import DataReader


class FileReader(DataReader):
    """
    FileReader class.

    The FileReader object tells the stores to fetch physical
    resources from backend and store them locally.
    """

    def fetch_data(self,
                   src: str) -> str:
        """
        Fetch resource from backend.
        """
        return self.store.fetch_file(src)
