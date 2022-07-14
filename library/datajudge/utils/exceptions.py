"""
Exceptions module.
"""


class DatajudgeError(Exception):
    """
    Base class for datajudge exception.
    """


class StoreError(DatajudgeError):
    """
    Raised when incontered errors on Stores.
    """


class RunError(DatajudgeError):
    """
    Raised when incontered errors on Runs.
    """


class ValidationError(DatajudgeError):
    """
    Raised when incontered errors on validation.
    """
