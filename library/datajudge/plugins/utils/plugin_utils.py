"""
Plugin utils module.
"""
import time
from collections import namedtuple
from typing import Any, Callable

from datajudge.utils.commons import STATUS_ERROR, STATUS_FINISHED, STATUS_INIT

RenderTuple = namedtuple("RenderTuple", ("object", "filename"))


class Result:
    """
    Simple class to aggregate result of plugin operation.
    """

    def __init__(
        self,
        status: str = STATUS_INIT,
        duration: float = None,
        errors: tuple = None,
        artifact: Any = None,
    ) -> None:
        self.status = status
        self.duration = duration
        self.errors = errors
        self.artifact = artifact


def exec_decorator(fnc: Callable) -> Result:
    """
    Decorator that keeps track of execution time and status.
    """

    def wrapper(*args, **kwargs) -> Result:
        """
        Wrapper.
        """
        data = Result()
        start = time.perf_counter()
        try:
            data.artifact = fnc(*args, **kwargs)
            data.status = STATUS_FINISHED
        except Exception as exc:
            data.errors = exc.args
            data.status = STATUS_ERROR
        data.duration = round(time.perf_counter() - start, 2)
        return data

    return wrapper


class ValidationReport:
    """
    Simple class to aggregate custom validation result.
    """

    def __init__(
        self,
        result: Any,
        valid: bool,
        error: list,
    ) -> None:
        self.result = result
        self.valid = valid
        self.error = error

    def to_dict(self):
        return {"result": self.result, "valid": self.valid, "error": self.error}
