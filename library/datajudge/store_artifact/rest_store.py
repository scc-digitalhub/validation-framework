"""
Implementation of rest artifact store.
"""
from typing import Any, IO, Optional, Tuple

from datajudge.store_artifact.artifact_store import ArtifactStore


class RestArtifactStore(ArtifactStore):
    """
    Rest artifact store object.

    Allows the client to interact with remote FTP/HTTP store.

    See also
    --------
    ArtifactStore : Abstract artifact store class.

    """

    def __init__(self,
                 artifact_uri: str,
                 config: Optional[dict] = None,
                 data: bool = False) -> None:
        super().__init__(artifact_uri, config, data)
        self._check_access_to_storage(self.artifact_uri)

    def persist_artifact(self,
                         src: Any,
                         dst: str,
                         src_name: str,
                         metadata: dict
                         ) -> Tuple[str, str]:
        """
        Persist an artifact.
        """

    def fetch_artifact(self, src: str) -> IO:
        """
        Method to fetch an artifact.
        """

    def _check_access_to_storage(self, dst: str) -> None:
        """
        Check if there is access to the storage.
        """

    def get_run_artifacts_uri(self, run_id: str) -> str:
        """
        Return the path of the artifact store for the Run.
        """
