# pylint: disable=import-error,no-name-in-module,arguments-differ,no-member,too-few-public-methods
from __future__ import annotations

import re
from typing import Any, Tuple

from datajudge.utils.commons import (CHECK_ROWS, CHECK_VALUE, EMPTY,
                                     EXACT, MAXIMUM, MINIMUM, NON_EMPTY, RANGE)
from datajudge.utils.exceptions import ValidationError


def evaluate_validity(query_result: Any,
                      check: str,
                      expect: str,
                      value: Any) -> Tuple[bool, list]:
    """
    Evaluate validity of query results.
    """
    try:

        if check == CHECK_VALUE:

            # Evaluation made on a single value as result of
            # a query.

            result = query_result.iloc[0, 0]

            if expect == EXACT:
                return evaluate_exact(result, value)
            elif expect == RANGE:
                return evaluate_range(result, value)
            elif expect == MINIMUM:
                return evaluate_min(result, value)
            elif expect == MAXIMUM:
                return evaluate_max(result, value)
            else:
                raise ValidationError("Invalid expectation.")

        elif check == CHECK_ROWS:

            # Evaluation made on number of rows

            result = query_result.shape[0]

            if expect == EMPTY:
                return evaluate_empty(result, empty=True)
            elif expect == NON_EMPTY:
                return evaluate_empty(result, empty=False)
            elif expect == EXACT:
                return evaluate_exact(result, value)
            elif expect == RANGE:
                return evaluate_range(result, value)
            elif expect == MINIMUM:
                return evaluate_min(result, value)
            elif expect == MAXIMUM:
                return evaluate_max(result, value)
            else:
                raise ValidationError("Invalid expectation.")

        else:
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
    else:
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


def evaluate_min(result: Any, value: Any) -> tuple:
    """
    Check if a value is bigger than a specific value.
    """
    if bool(float(result) >= value):
        return True, None
    return False, f"Minimum value {value}, instead got {result}."


def evaluate_max(result: Any, value: Any) -> tuple:
    """
    Check if a value is lesser than a specific value.
    """
    if bool(float(result) <= value):
        return True, None
    return False, f"Maximum value {value}, instead got {result}."


def evaluate_range(result: Any, _range: Any) -> tuple:
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
