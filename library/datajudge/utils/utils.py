from typing import Any, Tuple


def data_lister(data: Any,
                data_name: Any) -> Tuple[list, list]:
    """
    Check if the source is composed by multiple files.
    Return list of sources and sources names.
    """
    if not isinstance(data, list):
        data = [data]
    if data_name is None:
        data_name = [None for _, _ in enumerate(data)]
    elif isinstance(data_name, list):
        if not len(data) == len(data_name):
            raise IndexError("data name list must have " +
                             "same lenght of data source list")
    return data, data_name