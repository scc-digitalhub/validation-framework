"""
Results registry module.
It registers the results of execution for a named resource.
"""
from typing import Any, Optional


class ResultsRegistry:
    """
    Registry where to cache results over resources.
    """

    def __init__(self) -> None:
        self._registry = None
        self.setup()
   
    def setup(self):
        if self._registry is None:
            self._registry = {}
       
    def add_result(self,
                   res_name: str,
                   result: Any,
                   time: float) -> None:
        """
        Add new result to registry.
        """
        self._registry[res_name] = {
            "result": result,
            "time": time
        }
   
    def get_result(self,
                   res_name: str) -> Optional[Any]:
        """
        Get result for named resource.
        """
        return self._registry.get(res_name, {}).get("result")

    def get_time(self, res_name: str) -> Optional[float]:
        """
        Get execution time.
        """
        return self._registry.get(res_name, {}).get("time")
