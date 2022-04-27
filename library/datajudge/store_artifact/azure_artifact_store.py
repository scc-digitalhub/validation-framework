"""
Implementation of azure artifact store.
"""
# pylint: disable=import-error
import json
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any, IO

from azure.storage.blob import BlobServiceClient, ContainerClient

from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.file_utils import check_make_dir, check_path, get_path
from datajudge.utils.io_utils import wrap_string, write_bytes, write_bytesio
from datajudge.utils.uri_utils import (build_key, get_name_from_uri,
                                       get_uri_netloc, get_uri_path)


class AzureArtifactStore(ArtifactStore):
    """
    Azure artifact store object.

    Allows the client to interact with azure based storages.

    """
    def persist_artifact(self,
                         src: Any,
                         dst: str,
                         src_name: str,
                         metadata: dict
                         ) -> None:
        """
        Persist an artifact.
        """
        # Get container client
        client = self._get_client()
        self._check_access_to_storage(client)

        key = build_key(dst, src_name)

        # Local file
        if isinstance(src, (str, Path)) and check_path(src):
            self._upload_file(client, key, src, metadata)

        # Dictionary
        elif isinstance(src, dict) and src_name is not None:
            src = json.dumps(src)
            src = write_bytesio(src)
            self._upload_fileobj(client, key, src, metadata)

        # StringIO/BytesIO buffer
        elif isinstance(src, (BytesIO, StringIO)) and src_name is not None:
            src = wrap_string(src)
            self._upload_fileobj(client, key, src, metadata)

        else:
            raise NotImplementedError

    def fetch_artifact(self,
                       src: str, 
                       file_format: str) -> str:
        """
        Method to fetch an artifact.
        """
        # Get container client
        client = self._get_client()
        self._check_access_to_storage(client)

        key = get_uri_path(src)
        tmp_path = self.resource_paths.get_resource(key)
        if tmp_path is not None:
            return tmp_path
        
        # Get file from remote
        obj = self._get_object(client, key)

        # Store locally
        check_make_dir(self.temp_dir)
        name = get_name_from_uri(key)
        filepath = get_path(self.temp_dir, name)
        write_bytes(obj, filepath)

        # Register resource on store
        self.resource_paths.register(key, filepath)
        return filepath

    def _get_client(self) -> ContainerClient:
        """
        Return BlobServiceClient client.
        """
        container = get_uri_netloc(self.artifact_uri)
        
        if self.config is not None:
            conn_string = self.config.get("connection_string")
            acc_name = self.config.get("azure_account_name")
            acc_key = self.config.get("azure_access_key")

            # Check connection string
            if conn_string is not None:
                client = BlobServiceClient.from_connection_string(
                                                  conn_str=conn_string)
                return client.get_container_client(container)

            # Otherwise account name + key
            if acc_name is not None and acc_key is not None:
                url = f"https://{acc_name}.blob.core.windows.net"
                client = BlobServiceClient(account_url=url,
                                           credential=acc_key)
                return client.get_container_client(container)

        raise Exception("You must provide credentials!")

    def _check_access_to_storage(self, client: ContainerClient) -> None:
        """
        Check access to storage.
        """
        if not client.exists():
            raise RuntimeError("No access to Azure container!")

    def _upload_fileobj(self,
                        client: ContainerClient,
                        name: str,
                        data: IO,
                        metadata: dict) -> None:
        """
        Upload fileobj to Azure.
        """
        client.upload_blob(name=name,
                                data=data,
                                metadata=metadata,
                                overwrite=True)

    def _upload_file(self,
                     client: ContainerClient,
                     name: str,
                     path: str,
                     metadata: dict) -> None:
        """
        Upload file to Azure.
        """
        with open(path, "rb") as file:
            client.upload_blob(name=name,
                               data=file,
                               metadata=metadata,
                               overwrite=True)

    def _get_object(self,
                    client: ContainerClient,
                    path: str) -> bytes:
        """
        Download object from Azure.
        """
        return client.download_blob(path).readall()
