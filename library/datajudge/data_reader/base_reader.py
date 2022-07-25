"""
DataReader module.
"""
from __future__ import annotations

import typing
from abc import ABCMeta, abstractmethod
from typing import Any, Optional

from datajudge.utils.commons import (DATAREADER_BUFFER, DATAREADER_FILE,
                                     DATAREADER_NATIVE)

if typing.TYPE_CHECKING:
    from datajudge.store_artifact.artifact_store import ArtifactStore


class DataReader(metaclass=ABCMeta):
    """
    DataReader abstract class.

    This is the basic abstract class for the DataReaders.

    """

    FILE = DATAREADER_FILE
    NATIVE = DATAREADER_NATIVE
    BUFFER = DATAREADER_BUFFER

    def __init__(self,
                 store: ArtifactStore,
                 fetch_mode: str,
                 reader_args: Optional[dict] = None,
                 ) -> None:
        self.store = store
        self.fetch_mode = fetch_mode
        self.reader_args = reader_args

    @abstractmethod
    def fetch_resource(self,
                       src: str) -> Any:
        """
        Fetch resources from backend.
        """
