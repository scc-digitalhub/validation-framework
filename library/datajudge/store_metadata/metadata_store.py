"""
Abstract class for metadata store.
"""
import uuid
from abc import ABCMeta, abstractmethod
from typing import Optional

from datajudge.utils import config as cfg


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

    _RUN_METADATA = cfg.MT_RUN_METADATA
    _DATA_RESOURCE = cfg.MT_DATA_RESOURCE
    _SHORT_REPORT = cfg.MT_SHORT_REPORT
    _SHORT_SCHEMA = cfg.MT_SHORT_SCHEMA
    _DATA_PROFILE = cfg.MT_DATA_PROFILE
    _ARTIFACT_METADATA = cfg.MT_ARTIFACT_METADATA

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
