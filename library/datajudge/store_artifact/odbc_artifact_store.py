"""
Implementation of ODBC artifact store.
"""
# pylint: disable=import-error
from typing import Any

import pyarrow as pa
import pyarrow.parquet as pq
import pyodbc

from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.exceptions import StoreError
from datajudge.utils.file_utils import check_make_dir, get_path
from datajudge.utils.uri_utils import get_uri_netloc


class ODBCArtifactStore(ArtifactStore):
    """
    ODBC artifact store object.

    Allows the client to interact with ODBC storages.

    """

    def persist_artifact(
        self, src: Any, dst: str, src_name: str, metadata: dict
    ) -> None:
        """
        Method to persist an artifact.
        """
        raise NotImplementedError

    def _get_and_register_artifact(self, src: str, fetch_mode: str) -> str:
        """
        Method to fetch an artifact from the backend an to register
        it on the paths registry.
        """
        connection = self._get_connection()
        self._check_access_to_storage(connection)
        table_name = self._get_table_name(src)
        key = f"{table_name.lower()}.parquet"

        self.logger.info(f"Fetching resource {src} from store {self.name}")

        if fetch_mode == self.NATIVE:
            connection.close()
            raise NotImplementedError

        # Get file from remote and store locally
        if fetch_mode == self.FILE:
            obj = self._get_data(connection, table_name)
            filepath = self._store_data(obj, key)
            self._register_resource(f"{src}_{fetch_mode}", filepath)
            connection.close()
            return filepath

        if fetch_mode == self.BUFFER:
            connection.close()
            raise NotImplementedError

    def _check_access_to_storage(self, connection: pyodbc.Connection) -> None:
        """
        Check if there is access to the storage.
        """
        try:
            connection.cursor()
        except Exception:
            raise StoreError("No access to storage!")

    def _get_connection(self) -> pyodbc.Connection:
        """
        Create connection object from configuration.
        """
        try:
            return pyodbc.connect(**self.config)
        except Exception:
            raise StoreError("Something wrong with connection configuration.")

    @staticmethod
    def _get_table_name(uri: str) -> str:
        """
        Return table name from path.
        """
        return get_uri_netloc(uri)

    def _get_data(self, connection: pyodbc.Connection, table_full_name: str):
        """
        Return a table.
        """
        # Workaround to avoid sql injection. We check that the table name
        # provided by the user exists.
        sql = """
              SELECT  CONCAT(TABLE_SCHEMA, '.', TABLE_NAME) as table_full_name
              FROM    INFORMATION_SCHEMA.VIEWS
              """
        tables = connection.execute(sql).fetchall()
        table_list = list(map(lambda x: x[0], tables))
        if table_full_name in table_list:
            try:
                return connection.execute(f"SELECT * FROM {table_full_name}")
            except Exception as ex:
                raise StoreError(
                    f"Something wrong with data fetching. Arguments: {str(ex.args)}"
                )
        raise StoreError("Something wrong with resource name.")

    def _store_data(self, obj: Any, key: str) -> str:
        """
        Store data locally in temporary folder and return tmp path.
        """
        check_make_dir(self.temp_dir)
        filepath = get_path(self.temp_dir, key)
        self._write_table(obj, filepath)
        return filepath

    @staticmethod
    def _write_table(query_result: Any, filepath: str) -> None:
        """
        Write a query result as file.
        """
        header = [col[0] for col in query_result.description]
        arrays = []
        while True:
            res = query_result.fetchmany(1024)
            if res:
                for row in res:
                    arrays.append(dict(zip(header, row)))
            else:
                tab = pa.Table.from_pylist(arrays)
                pq.write_table(tab, filepath)
                break
