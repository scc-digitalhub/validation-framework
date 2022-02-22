"""
Common generic utils.
"""
import warnings
from datetime import datetime
from mimetypes import guess_type
from typing import Any, Optional, Tuple

import dateutil.parser as parser


def get_time() -> str:
    """
    Return ISO 8601 time with timezone info.
    """
    return datetime.now().astimezone().isoformat(timespec="milliseconds")


def time_to_sec(timestr: Optional[str] = None) -> float:
    """
    Convert a time string to a float.
    """
    if timestr is not None:
        parsed = parser.parse(timestr)
        total_time = (parsed.hour * 60 * 60 +
                      parsed.minute * 60 +
                      parsed.second +
                      parsed.microsecond / 1000000)
        return round(total_time, 4)


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


def guess_mediatype(path: str) -> str:
    """
    Guess mediatype of resource.
    """
    if isinstance(path, list):
        path = path[0]
    mtype, _ = guess_type(path)
    return mtype


def warn(msg: str):
    """
    Raise message warn.
    """
    warnings.warn(msg)
