"""
Dummy artifact store module.
"""
from typing import Any

from datajudge.store_artifact.artifact_store import ArtifactStore


class DummyArtifactStore(ArtifactStore):
    """
    Dummy artifact store object implementation.

    Allows the client to interact store methods.

    """
    def persist_artifact(self,
                         src: Any,
                         dst: str,
                         src_name: str,
                         metadata: dict
                         ) -> None:
        """
        Do nothing.
        """

    def fetch_artifact(self, src: str, dst: str) -> None:
        """
        Return none.
        """

    def _check_access_to_storage(self) -> None:
        """
        Do nothing.
        """

    def get_run_artifacts_uri(self,
                              exp_name: str,
                              run_id: str) -> None:
        """
        Return none.
        """
