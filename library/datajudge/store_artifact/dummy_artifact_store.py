"""
Dummy artifact store module.
"""
from datajudge.store_artifact.artifact_store import ArtifactStore


class DummyArtifactStore(ArtifactStore):
    """
    Dummy artifact store object implementation.

    Only allows the client to interact store methods.
    """

    def persist_artifact(self, *args) -> None: ...

    def _get_and_register_artifact(self, *args) -> None: ...

    def fetch_file(self, *args) -> None: ...

    def fetch_native(self, *args) -> None: ...

    def fetch_buffer(self, *args) -> None: ...

    def _check_access_to_storage(self, *args) -> None: ...

    def get_run_artifacts_uri(self, *args) -> None: ...

    def _get_data(self, *args) -> None: ...

    def _store_data(self, *args) -> None: ...
