"""
Implementation of REST metadata store designed by Digital Society Lab.
"""
# pylint: disable=import-error
from collections import namedtuple
from typing import Optional

from datajudge.store_metadata.metadata_store import MetadataStore


KeyPairs = namedtuple("KeyPairs", ("run_id", "key"))


class DummyMetadataStore(MetadataStore):
    """
    Dummy metadata store object implementation.

    Allows the client to interact store methods.

    """

    def init_run(self,
                 exp_name: str,
                 run_id: str,
                 overwrite: bool) -> None:
        """
        Do nothing.
        """

    def log_metadata(self,
                     metadata: dict,
                     dst: str,
                     src_type: str,
                     overwrite: bool) -> None:
        """
        Do nothing.
        """

    def _build_source_destination(self,
                                  dst: str,
                                  src_type: str,
                                  key: Optional[str] = None
                                  ) -> str:
        """
        Do nothing.
        """

    def get_run_metadata_uri(self,
                             exp_name: str,
                             run_id: str) -> str:
        """
        Return none.
        """
