"""
Implementation of ODBC artifact store.
"""
import csv
from typing import Any

import pyodbc

from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.exceptions import StoreError
from datajudge.utils.file_utils import check_make_dir, get_path
from datajudge.utils.uri_utils import get_table_path_from_uri


class ODBCArtifactStore(ArtifactStore):
    """
    ODBC artifact store object.

    Allows the client to interact with ODBC storages.

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
        connection = self._get_connection()
        self._check_access_to_storage(connection)
        
        table_name = get_table_path_from_uri(src)
        tmp_path = self.resource_paths.get_resource(table_name)
        if tmp_path is not None:
            return tmp_path
        
        # Query table and store locally
        obj = self._get_table(connection, table_name)
        check_make_dir(self.temp_dir)
        filepath = get_path(self.temp_dir, f"{table_name.lower()}.{file_format}")
        self._write_table(obj, filepath)
        connection.close()
        
        # Register resource on store
        self.resource_paths.register(table_name, filepath)
        return filepath

    def _check_access_to_storage(self,
                                 connection: pyodbc.Connection
                                 ) -> None:
        """
        Check if there is access to the storage.
        """
        try:
            connection.cursor()
        except Exception:
            raise StoreError("No access to storage!")

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
            raise StoreError("Something wrong with connection configuration.")

    def _get_table(self,
                   connection: pyodbc.Connection,
                   table_name: str):
        """
        Return a table.
        """
        return connection.execute("SELECT * FROM {}".format(table_name))

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
            header = [col[0] for col in obj.description]
            outcsv.writerow(header)
            outcsv.writerows(obj.fetchmany(256))
