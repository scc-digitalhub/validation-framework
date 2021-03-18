from abc import ABCMeta, abstractmethod
from typing import Any, Optional


class ArtifactStore:
    """
    Abstract artifact repo that defines how to persist
    artifacts from different storage backends.
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
        pass

    @abstractmethod
    def get_run_artifacts_uri(self, run_id: str) -> str:
        """Return the URI of the artifact store for the Run."""
        pass
