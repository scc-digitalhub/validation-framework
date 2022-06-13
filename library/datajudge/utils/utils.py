"""
Common generic utils.
"""
# pylint: disable=import-error
import functools
import logging
import operator
from datetime import datetime
from typing import Any, List, Optional, Tuple, Union
from uuid import uuid4

from frictionless import Schema

from datajudge.utils.config import ConstraintsFrictionless


# LOGGER
LOGGER = logging.getLogger("datajudge")
LOGGER.setLevel(logging.INFO)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
LOGGER.addHandler(ch)


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


def frictionless_schema_converter(schema: Union[dict, Schema],
                                  resource_name: str) -> List[ConstraintsFrictionless]:

    constraints = []
    for field in schema.get("fields", []):

        cnt = 0

        type_ = field.get("type")
        if type_ is not None:
            name = f'{field.get("name", "")}_{str(cnt)}'
            c = ConstraintsFrictionless(type="frictionless",
                                        name=name,
                                        resources=[resource_name],
                                        title=name,
                                        field=field.get("name"),
                                        fieldType=type_,
                                        constraint="type",
                                        value=type_,
                                        weight=5)
            constraints.append(c)
            cnt += 1

        format_ = field.get("format")
        if format_ is not None:
            name = f'{field.get("name", "")}_{str(cnt)}'
            c = ConstraintsFrictionless(type="frictionless",
                                        name=name,
                                        resources=[resource_name],
                                        title=name,
                                        field=field.get("name"),
                                        fieldType=type_,
                                        constraint="format",
                                        value=format_,
                                        weight=5)
            constraints.append(c)
            cnt += 1


        c_list = field.get("constraints", {})
        if c_list:
            for k, v in c_list.items():
                name = f'{field.get("name", "")}_{str(cnt)}'
                c = ConstraintsFrictionless(type="frictionless",
                                            name=name,
                                            resources=[resource_name],
                                            title=name,
                                            field=field.get("name"),
                                            fieldType=type_,
                                            constraint=k,
                                            value=v,
                                            weight=5)
                constraints.append(c)
                cnt += 1

    return constraints
