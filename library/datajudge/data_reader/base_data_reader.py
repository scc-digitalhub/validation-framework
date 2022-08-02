"""
DataReader module.
"""
from __future__ import annotations

import typing
from abc import ABCMeta, abstractmethod
from typing import Any, Optional

from datajudge.utils.logger import LOGGER

if typing.TYPE_CHECKING:
    from datajudge.store_artifact.artifact_store import ArtifactStore


class DataReader(metaclass=ABCMeta):
    """
    DataReader abstract class.

    This is the basic abstract class for the DataReaders.

    """

    def __init__(self,
                 store: ArtifactStore
                 ) -> None:
        self.store = store
        self.logger = LOGGER

    @abstractmethod
    def fetch_data(self,
                   src: str) -> Any:
        """
        Fetch resources from backend.
        """
