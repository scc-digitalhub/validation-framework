"""
BufferReader module.
"""
from datajudge.data_reader.base_data_reader import DataReader


class BufferReader(DataReader):
    """
    FileReader class.

    The FileReader object tells the stores to fetch physical
    resources from backend and store them locally or pass
    a string reference to the plugin according to store.
    """

    def fetch_data(self, src: str) -> bytes:
        """
        Fetch resource from backend as bytes.
        """
        return self.store.fetch_buffer(src)
