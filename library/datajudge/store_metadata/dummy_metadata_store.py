"""
Implementation of Dummy metadata store.
"""
from datajudge.store_metadata.metadata_store import MetadataStore


class DummyMetadataStore(MetadataStore):
    """
    Dummy metadata store object implementation.

    Only allows the client to interact with store methods.
    """

    def init_run(self, *args) -> None: ...

    def log_metadata(self, *args) -> None: ...

    def _build_source_destination(self, *args) -> None: ...

    def get_run_metadata_uri(self, *args) -> None: ...
