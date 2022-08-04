"""
DataReader module.
"""
from abc import ABCMeta, abstractmethod
from typing import Any

from datajudge.utils.logger import LOGGER


class DataReader(metaclass=ABCMeta):
    """
    DataReader abstract class.

    This is the basic abstract class for the DataReaders.

    """

    def __init__(self,
                 store: "ArtifactStore"
                 ) -> None:
        self.store = store
        self.logger = LOGGER

    @abstractmethod
    def fetch_data(self,
                   src: str) -> Any:
        """
        Fetch resources from backend.
        """
