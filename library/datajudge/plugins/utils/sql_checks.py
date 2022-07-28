"""
SQL checks module.
"""
from __future__ import annotations

import re
from typing import Any, Tuple, Union

from datajudge.utils.commons import (CONSTRAINT_SQL_CHECK_ROWS,
                                     CONSTRAINT_SQL_CHECK_VALUE,
                                     CONSTRAINT_SQL_EMPTY,
                                     CONSTRAINT_SQL_EXACT,
                                     CONSTRAINT_SQL_MAXIMUM,
                                     CONSTRAINT_SQL_MINIMUM,
                                     CONSTRAINT_SQL_NON_EMPTY,
                                     CONSTRAINT_SQL_RANGE)
from datajudge.utils.exceptions import ValidationError


def evaluate_validity(query_result: Any,
                      check: str,
                      expect: str,
                      value: Any) -> Tuple[bool, list]:
    """
    Evaluate validity of query results.
    """
    try:

        if check == CONSTRAINT_SQL_CHECK_VALUE:

            # Evaluation made on a single value as result of
            # a query.

            result = query_result.iloc[0, 0]

            if expect == CONSTRAINT_SQL_EXACT:
                return evaluate_exact(result, value)
            if expect == CONSTRAINT_SQL_RANGE:
                return evaluate_range(result, value)
            if expect == CONSTRAINT_SQL_MINIMUM:
                return evaluate_min(result, value)
            if expect == CONSTRAINT_SQL_MAXIMUM:
                return evaluate_max(result, value)
            raise ValidationError("Invalid expectation.")

        if check == CONSTRAINT_SQL_CHECK_ROWS:

            # Evaluation made on number of rows

            result = query_result.shape[0]

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
            raise ValidationError("Invalid expectation.")

        raise ValidationError("Invalid check typology.")

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
