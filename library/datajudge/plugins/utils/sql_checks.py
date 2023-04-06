"""
SQL checks module.
"""
import re
from collections import defaultdict
from typing import Any, Tuple, Union

from pandas import DataFrame as PdDataFrame
from polars import DataFrame as PlDataFrame

from datajudge.utils.commons import (CONSTRAINT_SQL_CHECK_ROWS,
                                     CONSTRAINT_SQL_CHECK_VALUE,
                                     CONSTRAINT_SQL_EMPTY,
                                     CONSTRAINT_SQL_EXACT,
                                     CONSTRAINT_SQL_MAXIMUM,
                                     CONSTRAINT_SQL_MINIMUM,
                                     CONSTRAINT_SQL_NON_EMPTY,
                                     CONSTRAINT_SQL_RANGE)


def filter_result(data: Union[PdDataFrame, PlDataFrame],
                  check: str) -> Any:
    """
    Return value or size of DataFrame for SQL checks.
    """
    if check == CONSTRAINT_SQL_CHECK_VALUE:
        if isinstance(data, PlDataFrame):
            return data[0, 0]
        if isinstance(data, PdDataFrame):
            return data.iloc[0, 0]

    if check == CONSTRAINT_SQL_CHECK_ROWS:
        return data.shape[0]


def evaluate_validity(result: Any,
                      expect: str,
                      value: Any) -> Tuple[bool, list]:
    """
    Evaluate validity of query results.
    """
    try:
        if expect == CONSTRAINT_SQL_EMPTY:
            return evaluate_empty(result, empty=True)
        if expect == CONSTRAINT_SQL_NON_EMPTY:
            return evaluate_empty(result, empty=False)
        if expect == CONSTRAINT_SQL_EXACT:
            return evaluate_exact(result, value)
        if expect == CONSTRAINT_SQL_RANGE:
            return evaluate_range(result, value)
        if expect == CONSTRAINT_SQL_MINIMUM:
            return evaluate_min(result, value)
        if expect == CONSTRAINT_SQL_MAXIMUM:
            return evaluate_max(result, value)

    except Exception as ex:
        return False, ex.args


def evaluate_empty(result: Any,
                   empty: bool) -> tuple:
    """
    Evaluate table emptiness.
    """
    # Could be done with evaluate_exact,
    # but we want a specific error.
    if empty:
        if result == 0:
            return True, None
        return False, "Table is not empty."
    if result > 0:
        return True, None
    return False, "Table is empty."


def evaluate_exact(result: Any, value: Any) -> tuple:
    """
    Evaluate if a value is exactly as expected.
    """
    if bool(result == value):
        return True, None
    return False, f"Expected value {value}, instead got {result}."


def evaluate_min(result: Union[int, float],
                 value: Union[int, float]) -> tuple:
    """
    Check if a value is bigger than a specific value.
    """
    if bool(float(result) >= value):
        return True, None
    return False, f"Minimum value {value}, instead got {result}."


def evaluate_max(result: Union[int, float],
                 value: Union[int, float]) -> tuple:
    """
    Check if a value is lesser than a specific value.
    """
    if bool(float(result) <= value):
        return True, None
    return False, f"Maximum value {value}, instead got {result}."


def evaluate_range(result: Any, _range: str) -> tuple:
    """
    Check if a value is in desired range.
    """
    regex = r"^(\[|\()([+-]?[0-9]+[.]?[0-9]*),\s?([+-]?[0-9]+[.]?[0-9]*)(\]|\))$"
    mtc = re.match(regex, _range)
    if mtc:
        # Upper and lower limit type
        # [ ] are inclusive
        # ( ) are exclusive
        ll = mtc.group(1)
        ul = mtc.group(4)

        # Minimum and maximum range values
        _min = float(mtc.group(2))
        _max = float(mtc.group(3))

        # Value to check to float
        cv = float(result)

        if ll == "[" and ul == "]":
            valid = (_min <= cv <= _max)
        elif ll == "[" and ul == ")":
            valid = (_min <= cv < _max)
        elif ll == "(" and ul == "]":
            valid = (_min < cv <= _max)
        elif ll == "(" and ul == ")":
            valid = (_min < cv < _max)

        if valid:
            return True, None
        return False, f"Expected value between {ll}{mtc.group(2)}, \
                        {mtc.group(3)}{ul}."
    return False, "Invalid range format."


def render_result(data: Union[PdDataFrame, PlDataFrame] = None
                  ) -> dict:
    """
    Parse a dataframe and return a dict.
    """
    if data is None:
        return {}

    # Set max result numbers to 100,
    # possibly extract logic from here

    # Parse polars dataframe
    if isinstance(data, PlDataFrame):
        part_data = data.head(100).to_dicts()
        _dict = defaultdict(list)
        for elm in part_data:
            for k, v in elm.items():
                _dict[k].append(v)
        return _dict

    # Parse pandas dataframe
    if isinstance(data, PdDataFrame):
        return data.head(100).to_dict()
