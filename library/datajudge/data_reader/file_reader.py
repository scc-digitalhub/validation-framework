"""
FileReader module.
"""
from typing import Any

from datajudge.data_reader.base_reader import DataReader
from datajudge.utils.exceptions import StoreError


class FileReader(DataReader):
    """
    FileReader class.

    The FileReader object tells the stores to fetch physical
    resources from backend and store them locally or pass
    a string reference to the plugin according to store.
    """

    def fetch_resource(self,
                       src: str) -> Any:
        """
        Fetch resource from backend.
        """
        if self.fetch_mode == self.FILE:
            return self.store.fetch_file(src)

        if self.fetch_mode == self.NATIVE:
            return self.store.fetch_native(src)

        if self.fetch_mode == self.BUFFER:
            return self.store.fetch_buffer(src)

        raise StoreError(
            "Please select a valid format to read file from backend.")
