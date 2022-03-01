from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Result:
    res_name: str
    exec_artifact: Any = None
    exec_result: str = None
    exec_time: float = None
    constraints: list = None


class PluginRegistry:
    """
    Registry where to cache results over resources.
    """

    def __init__(self) -> None:
        self._registry = {}

    def register_resource(self,
                          res_name: str) -> None:
        """
        Add resource on register.
        """
        if res_name not in self._registry:
            self._registry[res_name] = Result(res_name)

    def add_constraints(self,
                        res_name: str,
                        constraints: dict) -> None:
        """
        Add constraints to a resource.
        """
        self._registry[res_name].constraints = constraints

    def add_result(self,
                   res_name: str,
                   artifact: Any,
                   result: str,
                   time: Optional[float] = None
                   ) -> None:
        """
        Add new result to registry.
        """
        self._registry[res_name].exec_artifact = artifact
        self._registry[res_name].exec_result = result
        self._registry[res_name].exec_time = time

    def get_constraints(self,
                        res_name: str) -> dict:
        """
        Get constraints for a resource.
        """
        return self._registry.get(res_name, Result(res_name)).constraints

    def get_result(self,
                   res_name: str) -> Optional[Any]:
        """
        Get result for named resource.
        """
        return self._registry.get(res_name, Result(res_name)).exec_artifact
    
    def get_outcome(self,
                    res_name: str) -> Optional[str]:
        """
        Get outcome for named resource.
        """
        return self._registry.get(res_name, Result(res_name)).exec_result

    def get_time(self, res_name: str) -> Optional[float]:
        """
        Get execution time.
        """
        return self._registry.get(res_name, Result(res_name)).exec_time