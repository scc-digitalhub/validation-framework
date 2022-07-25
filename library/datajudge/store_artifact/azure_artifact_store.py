"""
Implementation of azure artifact store.
"""
import json
from datetime import datetime, timedelta
from io import BytesIO, StringIO
from pathlib import Path
from typing import IO, Any

from azure.storage.blob import (BlobSasPermissions, BlobServiceClient,
                                ContainerClient, generate_blob_sas)

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

    def _get_and_register_artifact(self,
                                   src: str,
                                   fetch_mode: str) -> str:
        """
        Method to fetch an artifact from the backend an to register
        it on the paths registry.
        """
        # Get container client and object key
        client = self._get_client()
        self._check_access_to_storage(client)
        key = get_uri_path(src)

        self.logger.info(f"Fetching resource {src} from store {self.name}")

        # Return a presigned URL
        if fetch_mode == self.NATIVE:
            url = self._get_presigned_url(client, key)
            self._register_resource(f"{src}_{fetch_mode}", url)
            return url

        # Get file from remote and store locally
        if fetch_mode == self.FILE:
            obj = self._get_data(client, key)
            filepath = self._store_data(obj, key)
            self._register_resource(f"{src}_{fetch_mode}", filepath)
            return filepath

        if fetch_mode == self.BUFFER:
            raise NotImplementedError

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

    @staticmethod
    def _check_access_to_storage(client: ContainerClient) -> None:
        """
        Check access to storage.
        """
        if not client.exists():
            raise RuntimeError("No access to Azure container!")

    @staticmethod
    def _get_presigned_url(client: ContainerClient,
                           src: str) -> str:
        """
        Encode credentials in Azure URI.
        """
        if src.startswith("/"):
            src = src[1:]
        read_sas_blob = generate_blob_sas(account_name=client.credential.account_name,
                                          container_name=client.container_name,
                                          blob_name=src,
                                          account_key=client.credential.account_key,
                                          permission=BlobSasPermissions(
                                              read=True),
                                          expiry=datetime.utcnow() + timedelta(hours=2))
        return f"{client.primary_endpoint}/{src}?{read_sas_blob}"

    @staticmethod
    def _upload_fileobj(client: ContainerClient,
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

    @staticmethod
    def _upload_file(client: ContainerClient,
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

    def _get_data(self,
                  client: ContainerClient,
                  key: str) -> bytes:
        """
        Download object from Azure.
        """
        return client.download_blob(key).readall()

    def _store_data(self,
                    obj: bytes,
                    key: str) -> str:
        """
        Store data locally in temporary folder and return tmp path.
        """
        check_make_dir(self.temp_dir)
        name = get_name_from_uri(key)
        filepath = get_path(self.temp_dir, name)
        write_bytes(obj, filepath)
        return filepath
