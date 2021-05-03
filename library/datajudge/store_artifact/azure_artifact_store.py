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
from datajudge.utils.uri_utils import (get_name_from_uri, get_uri_netloc,
                                       get_uri_path, new_uri_path)


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

        self.container = get_uri_netloc(self.artifact_uri)
        self._check_access_to_storage()

        # Get container client
        self.cont_client = self.client.get_container_client(self.container)

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
        key = new_uri_path(dst, src_name)

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

    @staticmethod
    def _store_fetched_artifact(obj: bytes,
                                dst: str) -> None:
        """
        Save artifact locally.
        """
        with open(dst, "wb") as file:
            file.write(obj)

    def _check_access_to_storage(self) -> None:
        """
        Check access to storage.
        """
        if not check_container(self.cont_client):
            raise RuntimeError("No access to Azure container!")

    def get_run_artifacts_uri(self, run_id: str) -> str:
        """
        Return the URI of the artifact store for the Run.
        """
        return new_uri_path(self.artifact_uri, run_id)

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
