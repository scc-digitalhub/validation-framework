"""
Implementation of S3 artifact store.
"""
# pylint: disable=import-error
import json
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any, Optional

import boto3

from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.exceptions import StoreError
from datajudge.utils.file_utils import check_make_dir, check_path, get_path
from datajudge.utils.io_utils import wrap_string, write_bytes, write_bytesio
from datajudge.utils.s3_utils import (check_bucket, get_object, s3_client,
                                      upload_file, upload_fileobj)
from datajudge.utils.uri_utils import (build_key, get_name_from_uri,
                                       get_uri_netloc, get_uri_path)


class S3ArtifactStore(ArtifactStore):
    """
    S3 artifact store object.

    Allows the client to interact with S3 based storages.

    """

    def __init__(self,
                 artifact_uri: str,
                 config: Optional[dict] = None
                 ) -> None:
        super().__init__(artifact_uri, config)

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
        key = build_key(dst, src_name)

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
        check_make_dir(dst)
        name = get_name_from_uri(key)
        filepath = get_path(dst, name)
        write_bytes(obj, filepath)
        return filepath

    def _check_access_to_storage(self) -> None:
        """
        Check access to storage.
        """
        if not check_bucket(self.client, self.bucket):
            raise StoreError("No access to s3 bucket!")

    def _get_client(self) -> s3_client:
        """
        Return boto client.
        """
        return boto3.client('s3', **self.config)
