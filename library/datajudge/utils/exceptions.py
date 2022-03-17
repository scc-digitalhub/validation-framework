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
        self.message = msg
        super().__init__(self.message)


class RunError(DatajudgeError):
    """
    Raised when incontered errors on Runs.
    """
    def __init__(self, msg: str):
        self.message = msg
        super().__init__(self.message)
