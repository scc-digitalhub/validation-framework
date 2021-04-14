import uuid
from abc import ABCMeta, abstractmethod
from typing import Optional

from datajudge.utils.constants import MetadataType


class MetadataStore:
    """
    Abstract metadata class that defines methods on how to persist
    metadata into different storage backends.

    Attributes
    ----------
    metadata_uri : str
        An URI string that points to the storage.
    config : dict, default = None
        A dictionary containing the credential needed to performs
        actions on the storage.

    Methods
    -------
    init_run :
        Check run enviroment existence.
    persist_metadata :
        Method that persist metadata.
    get_run_metadata_uri :
        Return the URI of the metadata store for the Run.
    get_data_resource_uri :
        Return the URI of the data resource for the Run.
    _build_source_destination :
        Return source destination based on source type.
    get_run_id :
        Return a string UID for a Run.

    """

    __metaclass__ = ABCMeta

    _RUN_METADATA = MetadataType.RUN_METADATA.value
    _DATA_RESOURCE = MetadataType.DATA_RESOURCE.value
    _SHORT_REPORT = MetadataType.SHORT_REPORT.value
    _SHORT_SCHEMA = MetadataType.SHORT_SCHEMA.value
    _DATA_PROFILE = MetadataType.DATA_PROFILE.value
    _ARTIFACT_METADATA = MetadataType.ARTIFACT_METADATA.value

    def __init__(self,
                 uri_metadata: str,
                 config:  Optional[dict] = None) -> None:
        self.uri_metadata = uri_metadata
        self.config = config

    @abstractmethod
    def init_run(self,
                 run_id: str,
                 overwrite: bool) -> None:
        """
        Initial enviroment operation.
        """

    @abstractmethod
    def log_metadata(self,
                     metadata: str,
                     dst: str,
                     src_type: str,
                     overwrite: bool) -> None:
        """
        Method that log metadata.
        """

    @abstractmethod
    def get_run_metadata_uri(self, run_id: str) -> str:
        """
        Return the URI of the metadata store for the Run.
        """

    @abstractmethod
    def get_data_resource_uri(self, run_id: str) -> str:
        """
        Return the URI of the data resource for the Run.
        """

    @abstractmethod
    def _build_source_destination(self,
                                  dst: str,
                                  src_type: str,
                                  key: Optional[str] = None) -> str:
        """
        Return source destination based on source type.
        """

    @staticmethod
    def get_run_id(run_id: Optional[str] = None) -> str:
        """
        Return a string UID for a Run.
        """
        if run_id:
            return run_id
        return uuid.uuid4().hex
