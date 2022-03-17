"""
Common generic utils.
"""
# pylint: disable=import-error
import uuid
from datetime import datetime
from typing import Any, List, Optional, Tuple, Union

from slugify import slugify


def get_uiid(_id: Optional[str] = None) -> str:
    """
    Return an UUID if not provided.
    """
    if _id:
        return _id
    return uuid.uuid4().hex


def get_slug(title: str) -> str:
    """
    Slugify a string.
    """
    return slugify(title, max_length=20, separator="_")


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
