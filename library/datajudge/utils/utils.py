"""
Common generic utils.
"""
# pylint: disable=import-error
import functools
import operator
import time
from datetime import datetime
from typing import Any, Callable, List, Optional, Tuple, Union
from uuid import uuid4

from datajudge.utils.config import STATUS_ERROR, STATUS_FINISHED


def exec_decorator(fnc: Callable) -> Tuple[Any, float]:
    """
    Decorator that keeps track of execution time and status.
    """
    def wrapper(*args, **kwargs) -> Tuple[Any, str, tuple, float]:
        """
        Wrapper.
        """
        start = time.perf_counter()
        try:
            result = fnc(*args, **kwargs)
            status = STATUS_FINISHED
            errors = None
        except Exception as exc:
            result = None
            status = STATUS_ERROR
            errors = exc.args
        end = round(time.perf_counter() - start, 2)
        return result, status, errors, end
    return wrapper


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
    return functools.reduce(operator.iconcat, list_of_list)


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
