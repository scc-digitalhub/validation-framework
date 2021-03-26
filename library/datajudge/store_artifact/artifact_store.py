from abc import ABCMeta, abstractmethod
from typing import Any, Optional


class ArtifactStore:
    """
    Abstract artifact class that defines methods to persist
    artifacts into different storage backends.

    Attributes
    ----------
    artifact_uri :
        An URI string that points to the storage.
    credentials :
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
                 credentials: Optional[dict] = None) -> None:
        self.artifact_uri = artifact_uri
        self.credentials = credentials

    @abstractmethod
    def persist_artifact(self,
                         src: Any,
                         dst: str,
                         src_name: str) -> None:
        """
        Method to persist an artifact.
        """
        pass

    @abstractmethod
    def _check_access_to_storage(self, args: Any) -> None:
        """
        Check if there is access to the storage.
        """
        pass

    @abstractmethod
    def get_run_artifacts_uri(self, run_id: str) -> str:
        """
        Return the URI of the artifact store for the Run.
        """
        pass
