"""
Abstract class for metadata store.
"""
from abc import ABCMeta, abstractmethod
from typing import Optional

from datajudge.utils import commons as cfg


class MetadataStore(metaclass=ABCMeta):
    """
    Abstract metadata class that defines methods on how to persist
    metadata into different storage backends.

    Attributes
    ----------
    name : str
        Name of store.
    type : str
        Type of store, e.g. http, local.
    metadata_uri : str
        An URI string that points to the storage.
    config : dict, default = None
        A dictionary with the credentials/configurations
        for the backend storage.

    """

    _RUN_METADATA = cfg.MT_RUN_METADATA
    _DJ_REPORT = cfg.MT_DJ_REPORT
    _DJ_SCHEMA = cfg.MT_DJ_SCHEMA
    _DJ_PROFILE = cfg.MT_DJ_PROFILE
    _ARTIFACT_METADATA = cfg.MT_ARTIFACT_METADATA
    _RUN_ENV = cfg.MT_RUN_ENV

    def __init__(
        self,
        name: str,
        store_type: str,
        metadata_uri: str,
        config: Optional[dict] = None,
    ) -> None:
        self.name = name
        self.store_type = store_type
        self.metadata_uri = metadata_uri
        self.config = config

    @abstractmethod
    def init_run(self, exp_name: str, run_id: str, overwrite: bool) -> None:
        """
        Initial enviroment operation.
        """

    @abstractmethod
    def log_metadata(
        self, metadata: str, dst: str, src_type: str, overwrite: bool
    ) -> None:
        """
        Method that log metadata.
        """

    @abstractmethod
    def get_run_metadata_uri(self, exp_name: str, run_id: str) -> str:
        """
        Return the URI of the metadata store for the Run.
        """

    @abstractmethod
    def _build_source_destination(
        self, dst: str, src_type: str, key: Optional[str] = None
    ) -> str:
        """
        Return source destination based on source type.
        """
