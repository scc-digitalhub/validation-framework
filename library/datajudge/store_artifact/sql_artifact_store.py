"""
Implementation of SQL artifact store.
"""
import csv
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.exceptions import StoreError
from datajudge.utils.file_utils import check_make_dir, get_path
from datajudge.utils.uri_utils import get_table_path_from_uri


class SQLArtifactStore(ArtifactStore):
    """
    SQL artifact store object.

    Allows the client to interact with SQL based storages.

    """
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

    def fetch_artifact(self,
                       src: str,
                       file_format: str) -> str:
        """
        Method to fetch an artifact.
        """
        engine = self._get_engine()
        self._check_access_to_storage(engine)

        table_name = get_table_path_from_uri(src)
        tmp_path = self.resource_paths.get_resource(table_name)
        if tmp_path is not None:
            return tmp_path

        # Query table and store locally
        obj = self._get_table(engine, table_name)
        check_make_dir(self.temp_dir)
        filepath = get_path(self.temp_dir, f"{table_name}.{file_format}")
        self._write_table(obj, filepath)

        engine.dispose()

        # Register resource on store
        self.resource_paths.register(table_name, filepath)
        return filepath

    def _check_access_to_storage(self,
                                 engine: Engine
                                 ) -> None:
        """
        Check if there is access to the storage.
        """
        try:
            engine.connect()
        except SQLAlchemyError:
            engine.dispose()
            raise StoreError("No access to db!")

    def _get_engine(self) -> Engine:
        """
        Create engine from connection string.
        """
        connection_string = self.config.get("connection_string")
        if connection_string is not None:
            return create_engine(connection_string)
        raise StoreError("Something wrong with connection string.")

    def _get_table(self,
                   engine: Engine,
                   table_name: str):
        """
        Return a table from a db.
        """
        return engine.execute("SELECT * FROM {}".format(table_name))

    @staticmethod
    def _write_table(obj: Any,
                     filepath: str) -> None:
        """
        Write a query result as csv.
        """
        with open(filepath, "w") as csvfile:
            outcsv = csv.writer(csvfile,
                                delimiter=',',
                                quotechar='"',
                                quoting=csv.QUOTE_MINIMAL)
            header = list(obj.keys())
            outcsv.writerow(header)
            outcsv.writerows(obj.fetchmany(256))
