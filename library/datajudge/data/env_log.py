"""
EnvLog module.
Basic log structure for execution enviroment.
"""
# pylint: disable=import-error
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
        return str(round(mem / (1024.0 ** 3)))+" GB"

    def dict(self) -> dict:
        """
        Return a dictionary.
        """
        env_data = {
            "platform": self.platform,
            "pythonVersion": self.python_version,
            "cpuModel": self.cpu_model,
            "cpuCore": self.cpu_core,
            "ram": self.ram
        }
        return env_data

    def __repr__(self) -> str:
        return str(self.dict())
