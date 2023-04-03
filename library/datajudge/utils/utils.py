"""
Common generic utils.
"""
import functools
import operator
from datetime import datetime
from typing import Any, List, Optional, Tuple, Union
from uuid import uuid4


def get_uiid(_id: Optional[str] = None) -> str:
    """
    Return an UUID if not provided.
    """
    if _id:
        return _id
    return uuid4().hex


def flatten_list(list_of_list: List[List[Any]]) -> List[Any]:
    """
    Flatten a list of list.
    """
    try:
        return functools.reduce(operator.iconcat, list_of_list)
    except TypeError:
        return []


def listify(obj: Union[List, Tuple, Any]) -> List[Any]:
    """
    Check if an object is a list or a tuple and return a list.
    """
    if not isinstance(obj, (list, tuple)):
        obj = [obj]
    return obj


def get_time() -> str:
    """
    Return ISO 8601 time with timezone info.
    """
    return datetime.now().astimezone().isoformat(timespec="milliseconds")
