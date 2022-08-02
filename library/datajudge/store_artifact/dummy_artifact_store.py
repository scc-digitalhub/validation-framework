"""
Dummy artifact store module.
"""
from typing import Any, Optional

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
                                   fetch_mode: str) -> str:
        """
        Return none.
        """

    def fetch_file(self, src: str) -> str:
        """
        Do nothing.
        """

    def fetch_native(self, src: str) -> str:
        """
        Do nothing.
        """

    def fetch_buffer(self, src: str) -> None:
        """
        Do nothing.
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
