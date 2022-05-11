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
    def __init__(self, msg: str):
        super().__init__(msg)


class RunError(DatajudgeError):
    """
    Raised when incontered errors on Runs.
    """
    def __init__(self, msg: str):
        super().__init__(msg)


class ValidationError(DatajudgeError):
    """
    Raised when incontered errors on validation.
    """
    def __init__(self, msg: str):
        super().__init__(msg)
