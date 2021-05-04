"""
Common generic utils.
"""
from datetime import datetime
from typing import Any, Tuple


def get_time() -> str:
    """
    Return string of datetime.now().
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def data_listify(data: Any,
                 data_name: Any) -> Tuple[list, list]:
    """
    Check if the source is composed by multiple files.
    Return list of sources and sources names.
    """
    if not isinstance(data, list):
        data = [data]
    if data_name is None:
        data_name = [None for _ in data]
    elif isinstance(data_name, list):
        if not len(data) == len(data_name):
            raise IndexError("Data filename list must have " +
                             "same lenght of data source list")
    return data, data_name
