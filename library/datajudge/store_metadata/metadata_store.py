import uuid
from abc import ABCMeta, abstractmethod
from typing import Optional


class MetadataStore:

    __metaclass__ = ABCMeta

    def __init__(self,
                 uri_metadata: str,
                 credentials:  Optional[dict] = None) -> None:
        self.uri_metadata = uri_metadata
        self.credentials = credentials

    @abstractmethod
    def create_run_enviroment(self,
                              run_id: str,
                              overwrite: bool) -> None:
        pass

    @abstractmethod
    def persist_metadata(self,
                         src: str,
                         dst: str,
                         src_type: str,
                         uid: Optional[str] = None) -> None:
        """
        Method that persist metadata into the store.
        """
        pass

    @abstractmethod
    def get_run_metadata_uri(self, run_id: str) -> str:
        """Return the URI for the run metadata"""
        pass

    @abstractmethod
    def get_data_resource_uri(self, run_id: str) -> str:
        pass

    @staticmethod
    @abstractmethod
    def _build_source_destination(src_type: str) -> str:
        """Return source destination based
        on source type."""
        pass

    @staticmethod
    def get_run_id(run_id: Optional[str] = None) -> str:
        """Return a string id for a Run."""
        if run_id:
            return run_id
        return uuid.uuid4().hex

    def __repr__(self) -> str:
        return str(self.__dict__)
