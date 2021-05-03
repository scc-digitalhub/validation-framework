"""
Implementation of S3 artifact store.
"""
import json
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any, Optional

# pylint: disable=import-error
import boto3
from botocore.client import Config
from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.file_utils import check_path, get_path
from datajudge.utils.io_utils import wrap_string, write_bytesio
from datajudge.utils.s3_utils import (check_bucket, get_object, upload_file,
                                      upload_fileobj)
from datajudge.utils.typing import s3_client
from datajudge.utils.uri_utils import (get_name_from_uri, get_uri_netloc,
                                       get_uri_path, new_uri_path)


class S3ArtifactStore(ArtifactStore):
    """
    S3 artifact store object.

    Allows the client to interact with S3 based storages.
    The credentials keys must be the same as the keywords arguments
    of boto3.client() method.

    Attributes
    ----------
    client :
        An S3 client to interact with the storage.

    """

    def __init__(self,
                 artifact_uri: str,
                 config: Optional[dict] = None,
                 data: bool = False) -> None:
        super().__init__(artifact_uri, config, data)

        self.client = self._get_client()

        self.bucket = get_uri_netloc(self.artifact_uri)
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
        key = new_uri_path(dst, src_name)

        # Local file
        if isinstance(src, (str, Path)) and check_path(src):
            upload_file(self.client, src, self.bucket, key, metadata)

        # Dictionary
        elif isinstance(src, dict) and src_name is not None:
            src = json.dumps(src)
            src = write_bytesio(src)
            upload_fileobj(self.client, src, self.bucket, key, metadata)

        # StringIO/BytesIO buffer
        elif isinstance(src, (BytesIO, StringIO)) and src_name is not None:
            src = wrap_string(src)
            upload_fileobj(self.client, src, self.bucket, key, metadata)

        else:
            raise NotImplementedError

    def fetch_artifact(self, src: str, dst: str) -> str:
        """
        Method to fetch an artifact.
        """
        # Get file from remote
        key = get_uri_path(src)
        obj = get_object(self.client, self.bucket, key)

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
        if not check_bucket(self.client, self.bucket):
            raise RuntimeError("No access to s3 bucket!")

    def get_run_artifacts_uri(self, run_id: str) -> str:
        """
        Return the URI of the artifact store for the Run.
        """
        return new_uri_path(self.artifact_uri, run_id)

    def _get_client(self) -> s3_client:
        """
        Return boto client.
        """
        return boto3.client('s3',
                            config=Config(signature_version='s3v4'),
                            region_name='us-east-1',
                            **self.config)
