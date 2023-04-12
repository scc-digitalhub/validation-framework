import pytest

from datajudge.utils.exceptions import (
    DatajudgeError,
    StoreError,
    RunError,
    ValidationError,
)


def test_datajudge_error():
    with pytest.raises(DatajudgeError):
        raise DatajudgeError("Datajudge error occurred")


def test_store_error():
    with pytest.raises(StoreError):
        raise StoreError("Store error occurred")


def test_run_error():
    with pytest.raises(RunError):
        raise RunError("Run error occurred")


def test_validation_error():
    with pytest.raises(ValidationError):
        raise ValidationError("Validation error occurred")


def test_subclass():
    assert issubclass(StoreError, DatajudgeError)
    assert issubclass(RunError, DatajudgeError)
    assert issubclass(ValidationError, DatajudgeError)
