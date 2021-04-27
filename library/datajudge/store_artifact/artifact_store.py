"""
Abstract class for artifact store.
"""
from abc import ABCMeta, abstractmethod
from io import BytesIO
from typing import Any, Optional

from datajudge.utils.file_utils import check_dir, make_dir


class ArtifactStore:
    """
    Abstract artifact class that defines methods to persist
    artifacts into different storage backends.

    Attributes
    ----------
    artifact_uri : str
        An URI string that points to the storage.
    config : dict, default = None
        A dictionary containing the credential needed to performs
        actions on the storage.

    Methods
    -------
    persist_artifact :
        Method to persist an artifact.
    _check_access_to_storage :
        Check if there is access to the storage.
    get_run_artifacts_uri :
        Return the URI of the artifact store for the Run.

    """

    __metaclass__ = ABCMeta

    def __init__(self,
                 artifact_uri: str,
                 config: Optional[dict] = None,
                 data: bool = False) -> None:
        self.artifact_uri = artifact_uri
        self.config = config
        self.data = data

    @abstractmethod
    def persist_artifact(self,
                         src: Any,
                         dst: str,
                         src_name: str) -> None:
        """
        Method to persist an artifact.
        """

    @abstractmethod
    def fetch_artifact(self, src: str, dst: str) -> BytesIO:
        """
        Method to fetch an artifact.
        """

    @abstractmethod
    def _check_access_to_storage(self) -> None:
        """
        Check if there is access to the storage.
        """

    @abstractmethod
    def get_run_artifacts_uri(self, run_id: str) -> str:
        """
        Return the URI of the artifact store for the Run.
        """

    @staticmethod
    def _check_temp_dir(uri: str) -> None:
        """
        Check if temp dir already exist, otherwise create it.
        """
        if not check_dir(uri):
            make_dir(uri)
