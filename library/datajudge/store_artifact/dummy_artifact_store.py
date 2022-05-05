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

    def _get_and_register_artifact(self,
                                   src: str,
                                   file_format: str) -> str:
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

    def _get_data(self, *args) -> Any:
        """
        Do nothing.
        """

    def _store_data(self, *args) -> str:
        """
        Do nothing.
        """
