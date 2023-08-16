"""
EnvLog module.
Basic log structure for execution enviroment.
"""
import os
import platform

from psutil import virtual_memory


class EnvLog:
    """
    Basic log structure for execution enviroment.
    """

    def __init__(self) -> None:
        self.platform = platform.platform()
        self.python_version = platform.python_version()
        self.cpu_model = platform.processor()
        self.cpu_core = os.cpu_count()
        self.ram = self.round_ram()

    @staticmethod
    def round_ram() -> str:
        """
        Return rounded GB ram memory.
        """
        mem = virtual_memory().total
        return str(round(mem / (1024.0**3))) + " GB"

    def to_dict(self) -> dict:
        """
        Return a dictionary.
        """
        return self.__dict__

    def __repr__(self) -> str:
        return str(self.to_dict())
