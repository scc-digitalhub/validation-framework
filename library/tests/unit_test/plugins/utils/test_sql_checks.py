from datajudge.plugins.utils.sql_checks import (
    evaluate_empty,
    evaluate_exact,
    evaluate_max,
    evaluate_min,
    evaluate_range,
    evaluate_validity,
)

from datajudge.utils.commons import (
    CONSTRAINT_SQL_EMPTY,
    CONSTRAINT_SQL_EXACT,
    CONSTRAINT_SQL_MAXIMUM,
    CONSTRAINT_SQL_MINIMUM,
    CONSTRAINT_SQL_NON_EMPTY,
    CONSTRAINT_SQL_RANGE,
)


def test_evaluate_validity():
    assert evaluate_validity(0, CONSTRAINT_SQL_EMPTY, None) == (True, None)
    assert evaluate_validity(5, CONSTRAINT_SQL_EMPTY, None) == (
        False,
        "Table is not empty.",
    )
    assert evaluate_validity(7, CONSTRAINT_SQL_NON_EMPTY, None) == (True, None)
    assert evaluate_validity(0, CONSTRAINT_SQL_NON_EMPTY, None) == (
        False,
        "Table is empty.",
    )
    assert evaluate_validity(4, CONSTRAINT_SQL_EXACT, 4) == (True, None)
    assert evaluate_validity(2.1, CONSTRAINT_SQL_EXACT, 2.0) == (
        False,
        "Expected value 2.0, instead got 2.1.",
    )
    assert evaluate_validity(3, CONSTRAINT_SQL_MINIMUM, 2) == (True, None)
    assert evaluate_validity(4.8, CONSTRAINT_SQL_MINIMUM, 4.9) == (
        False,
        "Minimum value 4.9, instead got 4.8.",
    )
    assert evaluate_validity(-1, CONSTRAINT_SQL_MINIMUM, -3) == (True, None)
    assert evaluate_validity(6, CONSTRAINT_SQL_MAXIMUM, 7) == (True, None)
    assert evaluate_validity(9.9, CONSTRAINT_SQL_MAXIMUM, 10.1) == (True, None)
    assert evaluate_validity(25, CONSTRAINT_SQL_MAXIMUM, 15) == (
        False,
        "Maximum value 15, instead got 25.",
    )
    assert evaluate_validity(5.6, CONSTRAINT_SQL_RANGE, "[4, 9]") == (True, None)
    assert evaluate_validity(13, CONSTRAINT_SQL_RANGE, "[5, 12]") == (
        False,
        "Expected value between [5, 12].",
    )
    assert evaluate_validity("test", "INCORRECT", None) == (
        False,
        "Invalid constraint expectation.",
    )


def test_evaluate_empty():
    assert evaluate_empty(0, True) == (True, None)
    assert evaluate_empty(5, True) == (False, "Table is not empty.")
    assert evaluate_empty(7, False) == (True, None)
    assert evaluate_empty(0, False) == (False, "Table is empty.")


def test_evaluate_exact():
    assert evaluate_exact(4, 4) == (True, None)
    assert evaluate_exact("test", "test") == (True, None)
    assert evaluate_exact(2.1, 2.0) == (False, "Expected value 2.0, instead got 2.1.")


def test_evaluate_min():
    assert evaluate_min(3, 2) == (True, None)
    assert evaluate_min(4.8, 4.9) == (False, "Minimum value 4.9, instead got 4.8.")
    assert evaluate_min(-1, -3) == (True, None)


def test_evaluate_max():
    assert evaluate_max(6, 7) == (True, None)
    assert evaluate_max(9.9, 10.1) == (True, None)
    assert evaluate_max(25, 15) == (False, "Maximum value 15, instead got 25.")


def test_evaluate_range_valid_input():
    assert evaluate_range(5.6, "[4, 9]") == (True, None)
    assert evaluate_range(2.8, "[-10, -1)") == (
        False,
        "Expected value between [-10, -1).",
    )
    assert evaluate_range(3.14, "(2, 4)") == (True, None)


def test_evaluate_range_invalid_input():
    assert evaluate_range(-7, "[2, 10)") == (False, "Expected value between [2, 10).")
    assert evaluate_range(13, "[5, 12]") == (False, "Expected value between [5, 12].")
    assert evaluate_range("bad input", "(0, 1)") == (False, "Invalid range format.")
