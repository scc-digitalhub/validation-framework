"""
Implementation of SQL artifact store.
"""
from typing import Any, Optional

import sqlalchemy
from sqlalchemy import create_engine

from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.exceptions import StoreError
from datajudge.utils.file_utils import check_make_dir, get_path, write_table
from datajudge.utils.sql_utils import get_table
from datajudge.utils.uri_utils import get_table_path_from_uri


class SQLArtifactStore(ArtifactStore):
    """
    S3 artifact store object.

    Allows the client to interact with S3 based storages.

    """


    def __init__(self,
                 artifact_uri: str,
                 config: Optional[dict] = None
                 ) -> None:
        super().__init__(artifact_uri, config)
        self.engine = self._get_engine()

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
        obj = get_table(self.engine, table_name)

        # Store locally
        check_make_dir(dst)
        filepath = get_path(dst, f"{table_name}.csv")
        import pdb; pdb.set_trace()
        write_table(obj, filepath)
        return filepath

    def _check_access_to_storage(self) -> None:
        """
        Check if there is access to the storage.
        """
        try:
            self.engine.connect()
        except Exception:
            raise StoreError("No access to db!")

    def _get_engine(self) -> sqlalchemy.engine.Engine:
        """
        Create engine from configuartion.
        """
        connection_string = self.config.get("connection_string")
        if connection_string is not None:
            return create_engine(connection_string)
        raise StoreError("Something wrong with connection string.")
