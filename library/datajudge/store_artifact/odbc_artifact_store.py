"""
Implementation of ODBC artifact store.
"""
import csv
from typing import Any

import pyodbc
import pyarrow as pa
import pyarrow.parquet as pq

from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.exceptions import StoreError
from datajudge.utils.file_utils import check_make_dir, get_path
from datajudge.utils.uri_utils import get_uri_netloc


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
        
        table_name = self._get_table_name(src)
        tmp_path = self.resource_paths.get_resource(table_name)
        if tmp_path is not None:
            return tmp_path
        
        # Query table and store locally
        check_make_dir(self.temp_dir)
        filepath = get_path(self.temp_dir, f"{table_name.lower()}.{file_format}")
        obj = self._get_data(connection, table_name)
        self._write_table(obj, filepath, file_format)

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

    @staticmethod
    def _get_table_name(uri: str) -> str:
        """
        Return table name from path.
        """
        return get_uri_netloc(uri)

    def _get_data(self,
                  connection: pyodbc.Connection,
                  table_full_name: str):
        """
        Return a table.
        """        
        sql = """
              SELECT  CONCAT(TABLE_SCHEMA, '.', TABLE_NAME) as table_full_name
              FROM    INFORMATION_SCHEMA.VIEWS
              """

        # Workaround to avoid sql injection. We check that the table name
        # provided by the user exists.
        tables = connection.execute(sql).fetchall()
        table_list = list(map(lambda x: x[0], tables))
        if table_full_name in table_list:
            try:
                return connection.execute(f"SELECT * FROM {table_full_name}")
            except Exception:
                raise StoreError("Something wrong with data fetching.")
        raise StoreError("Something wrong with resource name.")

    @staticmethod
    def _write_table(query_result: Any,
                     filepath: str,
                     file_format: str) -> None:
        """
        Persist a query result.
        """
        header = [col[0] for col in query_result.description]

        if file_format == "csv":  
            with open(filepath, "w") as csvfile:
                outcsv = csv.writer(csvfile,
                                    delimiter=',',
                                    quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
                outcsv.writerow(header)
                while True:
                    res = query_result.fetchmany(1028)
                    if res:
                        outcsv.writerows(res)
                    else:
                        break

        elif file_format == "parquet":
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
