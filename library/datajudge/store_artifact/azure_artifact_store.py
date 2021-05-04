"""
Implementation of azure artifact store.
"""
import json
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any, Optional

# pylint: disable=import-error
from azure.storage.blob import BlobServiceClient
from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.azure_utils import (check_container, get_object,
                                         upload_file, upload_fileobj)
from datajudge.utils.file_utils import check_path, get_path
from datajudge.utils.io_utils import wrap_string, write_bytesio
from datajudge.utils.uri_utils import (build_key, get_name_from_uri, get_uri_netloc,
                                       get_uri_path, rebuild_uri)


class AzureArtifactStore(ArtifactStore):
    """
    Azure artifact store object.

    Allows the client to interact with azure based storages.
    The credentials keys ...

    Attributes
    ----------
    client :
        An Azure BlobServiceClient client to interact with the
        storage.

    """

    def __init__(self,
                 artifact_uri: str,
                 config: Optional[dict] = None,
                 data: bool = False) -> None:
        super().__init__(artifact_uri, config, data)
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
            upload_file(self.cont_client, key, src, metadata)

        # Dictionary
        elif isinstance(src, dict) and src_name is not None:
            src = json.dumps(src)
            src = write_bytesio(src)
            upload_fileobj(self.cont_client, key, src, metadata)

        # StringIO/BytesIO buffer
        elif isinstance(src, (BytesIO, StringIO)) and src_name is not None:
            src = wrap_string(src)
            upload_fileobj(self.cont_client, key, src, metadata)

        else:
            raise NotImplementedError

    def fetch_artifact(self, src: str, dst: str) -> str:
        """
        Method to fetch an artifact.
        """
        # Get file from remote
        key = get_uri_path(src)
        obj = get_object(self.cont_client, key)

        # Store locally
        self._check_temp_dir(dst)
        name = get_name_from_uri(key)
        filepath = get_path(dst, name)
        self._store_fetched_artifact(obj, filepath)
        return filepath

    def _check_access_to_storage(self) -> None:
        """
        Check access to storage.
        """
        if not check_container(self.cont_client):
            raise RuntimeError("No access to Azure container!")

    def _get_client(self) -> BlobServiceClient:
        """
        Return BlobServiceClient client.
        """
        if "connection_string" in self.config:
            client = BlobServiceClient.from_connection_string(
                conn_str=self.config["connection_string"]
            )
        elif ("azure_account_name" in self.config and
              "azure_access_key" in self.config):
            name = self.config['azure_account_name']
            url = f"https://{name}.blob.core.windows.net"
            client = BlobServiceClient(
                account_url=url,
                credential=self.config["azure_access_key"]
            )
        else:
            raise Exception(
                "You need to provide valid credentials!"
            )
        return client
