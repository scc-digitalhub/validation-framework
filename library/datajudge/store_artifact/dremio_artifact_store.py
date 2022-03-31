"""
Implementation of Dremio artifact store.
"""
from typing import Any, Optional

import pyodbc

from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.exceptions import StoreError
from datajudge.utils.file_utils import check_make_dir, get_path
from datajudge.utils.io_utils import write_dremio_table
from datajudge.utils.sql_utils import get_table_dremio
from datajudge.utils.uri_utils import get_table_path_from_uri


class DremioArtifactStore(ArtifactStore):
    """
    Dremio artifact store object.

    Allows the client to interact with Dremio storages.

    """

    def __init__(self,
                 artifact_uri: str,
                 config: Optional[dict] = None
                 ) -> None:
        super().__init__(artifact_uri, config)
        self.conn = self._get_connection()

    def persist_artifact(self,
                         src: Any,
                         dst: str,
                         src_name: str,
                         metadata: dict
                         ) -> None:
        """
        Method to persist an artifact.
        """
        raise NotImplementedError

    def fetch_artifact(self, src: str, dst: str) -> str:
        """
        Method to fetch an artifact.
        """
        # Query table
        table_name = get_table_path_from_uri(src)
        obj = get_table_dremio(self.conn, table_name)

        # Store locally
        check_make_dir(dst)
        filepath = get_path(dst, f"{table_name.lower()}.csv")
        write_dremio_table(obj, filepath)
        return filepath

    def _check_access_to_storage(self) -> None:
        """
        Check if there is access to the storage.
        """
        try:
            self.conn.cursor()
        except Exception:
            raise StoreError("No access to dremio!")

    def _get_connection(self) -> pyodbc.Connection:
        """
        Create engine from connection string.
        """
        try:
            return pyodbc.connect(driver=self.config.get("driver"),
                                  host=self.config.get("host"),
                                  port=self.config.get("port"),
                                  user=self.config.get("user"),
                                  password=self.config.get("password"),
                                  autocommit=True)
        except Exception:
            raise StoreError("Something wrong with connection.")
