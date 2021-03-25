import uuid
from abc import ABCMeta, abstractmethod
from typing import Optional


class MetadataStore:
    """
    Abstract metadata repo that defines methods on how to persist
    metadata into different storage backends.

    Attributes
    ----------
    metadata_uri :
        An URI string that points to the storage.
    credentials :
        A dictionary containing the credential needed to performs
        actions on the storage.

    Methods
    -------
    persist_metadata :
        Method that persist metadata.
    check_run :
        Check run id existence.
    get_run_metadata_uri :
        Return the URI of the metadata store for the Run.
    get_data_resource_uri :
        Return the URI of the data resource for the Run.
    _build_source_destination :
        Return source destination based on source type
    get_run_id :
        Return a string id for a Run.

    """

    __metaclass__ = ABCMeta

    def __init__(self,
                 uri_metadata: str,
                 credentials:  Optional[dict] = None) -> None:
        self.uri_metadata = uri_metadata
        self.credentials = credentials

    @abstractmethod
    def check_run(self,
                  run_id: str,
                  overwrite: Optional[bool] = False) -> None:
        """
        Check run id existence.
        """
        pass

    @abstractmethod
    def persist_metadata(self,
                         metadata: str,
                         dst: str,
                         src_type: str) -> None:
        """
        Method that persist metadata.
        """
        pass

    @abstractmethod
    def get_run_metadata_uri(self, run_id: str) -> str:
        """
        Return the URI of the metadata store for the Run.
        """
        pass

    @abstractmethod
    def get_data_resource_uri(self, run_id: str) -> str:
        """
        Return the URI of the data resource for the Run.
        """
        pass

    @staticmethod
    @abstractmethod
    def _build_source_destination(dst: str,
                                  src_type: str) -> str:
        """
        Return source destination based on source type.
        """
        pass

    @staticmethod
    def get_run_id(run_id: Optional[str] = None) -> str:
        """
        Return a string id for a Run.
        """
        if run_id:
            return run_id
        return uuid.uuid4().hex

    def __repr__(self) -> str:
        return str(self.__dict__)
