"""
Implementation of azure artifact store.
"""
# pylint: disable=import-error
import json
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any, IO, Optional

from azure.storage.blob import BlobServiceClient

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
    def __init__(self,
                 artifact_uri: str,
                 temp_dir: str,
                 config: Optional[dict] = None
                 ) -> None:
        super().__init__(artifact_uri, temp_dir, config)
        # Get BlobService Client
        self.client = self._get_client()

        # Get container client
        self.container = get_uri_netloc(self.artifact_uri)
        self.cont_client = self.client.get_container_client(self.container)

        self._check_access_to_storage()

    def persist_artifact(self,
                         src: Any,
                         dst: str,
                         src_name: str,
                         metadata: dict
                         ) -> None:
        """
        Persist an artifact.
        """
        self._check_access_to_storage()
        key = build_key(dst, src_name)

        # Local file
        if isinstance(src, (str, Path)) and check_path(src):
            self._upload_file(key, src, metadata)

        # Dictionary
        elif isinstance(src, dict) and src_name is not None:
            src = json.dumps(src)
            src = write_bytesio(src)
            self._upload_fileobj(key, src, metadata)

        # StringIO/BytesIO buffer
        elif isinstance(src, (BytesIO, StringIO)) and src_name is not None:
            src = wrap_string(src)
            self._upload_fileobj(key, src, metadata)

        else:
            raise NotImplementedError

    def fetch_artifact(self, src: str, dst: str) -> str:
        """
        Method to fetch an artifact.
        """
        # Get file from remote
        key = get_uri_path(src)
        obj = self._get_object(key)

        # Store locally
        check_make_dir(dst)
        name = get_name_from_uri(key)
        filepath = get_path(dst, name)
        write_bytes(obj, filepath)
        return filepath

    def _check_access_to_storage(self) -> None:
        """
        Check access to storage.
        """
        if not self._check_container():
            raise RuntimeError("No access to Azure container!")

    def _get_client(self) -> BlobServiceClient:
        """
        Return BlobServiceClient client.
        """
        if self.config is not None:
            conn_string = self.config.get("connection_string")
            acc_name = self.config.get("azure_account_name")
            acc_key = self.config.get("azure_access_key")

            # Check connection string
            if conn_string is not None:
                return BlobServiceClient.from_connection_string(
                                                  conn_str=conn_string)

            # Otherwise account name + key
            if acc_name is not None and acc_key is not None:
                url = f"https://{acc_name}.blob.core.windows.net"
                return BlobServiceClient(account_url=url,
                                         credential=acc_key)

        raise Exception("You must provide credentials!")

    def _check_container(self) -> bool:
        """
        Check access to a container.
        """
        return self.client.exists()

    def _upload_fileobj(self,
                        name: str,
                        data: IO,
                        metadata: dict) -> None:
        """
        Upload fileobj to Azure.
        """
        self.client.upload_blob(name=name,
                                data=data,
                                metadata=metadata,
                                overwrite=True)

    def _upload_file(self,
                    name: str,
                    path: str,
                    metadata: dict) -> None:
        """
        Upload file to Azure.
        """
        with open(path, "rb") as file:
            self.client.upload_blob(name=name,
                                    data=file,
                                    metadata=metadata,
                                    overwrite=True)

    def _get_object(self,
                    path: str) -> bytes:
        """
        Download object from Azure.
        """
        return self.client.download_blob(path).readall()
