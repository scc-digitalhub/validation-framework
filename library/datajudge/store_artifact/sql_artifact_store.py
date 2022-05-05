"""
Implementation of SQL artifact store.
"""
import csv
from typing import Any, Optional

import pyarrow as pa
import pyarrow.parquet as pq
from sqlalchemy import MetaData, Table, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.exc import SQLAlchemyError

from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.exceptions import StoreError
from datajudge.utils.file_utils import check_make_dir, get_path
from datajudge.utils.uri_utils import get_uri_netloc


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

    def _get_and_register_artifact(self,
                                   src: str,
                                   file_format: str) -> str:
        """
        Method to fetch an artifact from the backend an to register
        it on the paths registry.
        """
        engine = self._get_engine()
        self._check_access_to_storage(engine)
        table_name = self._get_table_name(src)
        schema = self._get_schema(src)
        key = f"{schema}.{table_name}.{file_format}"

        # Query table
        obj = self._get_data(engine, table_name, schema)

        # Store locally
        filepath = self._store_data(obj, key, file_format)

        # Dispose engine
        engine.dispose()

        # Register resource on store
        self._register_resource(f"{src}_{file_format}", filepath)
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
            return create_engine(connection_string, future=True)
        raise StoreError("Something wrong with connection string.")

    @staticmethod
    def _get_table_name(uri: str) -> str:
        """
        Return table name from path.
        """
        name = get_uri_netloc(uri)
        return name.split(".")[-1]

    @staticmethod
    def _get_schema(uri: str) -> str:
        """
        Try to get schema from configuration.
        """
        name = get_uri_netloc(uri)
        return name.split(".")[0]

    def _get_data(self,
                  engine: Engine,
                  table_name: str,
                  schema: Optional[str] = None
                  ) -> CursorResult:
        """
        Return a table from a db.
        """
        metadata = MetaData(bind=engine, schema=schema)
        table = Table(table_name, metadata, autoload=True)
        query = table.select()
        with engine.connect() as conn:
            results = conn.execute(query)
        return results

    def _store_data(self,
                    obj: CursorResult,
                    key: str,
                    file_format: str) -> str:
        """
        Store data locally in temporary folder and return tmp path.
        """
        check_make_dir(self.temp_dir)
        filepath = get_path(self.temp_dir, key)
        self._write_table(obj, filepath, file_format)
        return filepath

    @staticmethod
    def _write_table(query_result: CursorResult,
                     filepath: str,
                     file_format: str) -> None:
        """
        Write a query result as csv.
        """
        if file_format == "csv":
            with open(filepath, "w") as csvfile:
                outcsv = csv.writer(csvfile,
                                    delimiter=',',
                                    quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
                header = list(query_result.keys())
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
                    arrays.extend(list(map(lambda x: dict(x), res)))
                else:
                    tab = pa.Table.from_pylist(arrays)
                    pq.write_table(tab, filepath)
                    break
