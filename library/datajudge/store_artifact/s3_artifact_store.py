"""
Implementation of S3 artifact store.
"""
# pylint: disable=unused-import
import json
from io import BytesIO, StringIO
from pathlib import Path
from typing import IO, Any, Type

import boto3
import botocore.client
from botocore.exceptions import ClientError

from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.exceptions import StoreError
from datajudge.utils.file_utils import check_make_dir, check_path, get_path
from datajudge.utils.io_utils import wrap_string, write_bytes, write_bytesio
from datajudge.utils.uri_utils import (
    build_key,
    get_name_from_uri,
    get_uri_netloc,
    get_uri_path,
)

S3Client = Type["botocore.client.S3"]


class S3ArtifactStore(ArtifactStore):
    """
    S3 artifact store object.

    Allows the client to interact with S3 based storages.

    """

    def persist_artifact(
        self, src: Any, dst: str, src_name: str, metadata: dict
    ) -> None:
        """
        Persist an artifact.
        """
        client = self._get_client()
        bucket = get_uri_netloc(self.artifact_uri)
        self._check_access_to_storage(client, bucket)

        key = build_key(dst, src_name)

        # Local file
        if isinstance(src, (str, Path)) and check_path(src):
            self._upload_file(client, bucket, str(src), key, metadata)

        # Dictionary
        elif isinstance(src, dict) and src_name is not None:
            src = json.dumps(src)
            src = write_bytesio(src)
            self._upload_fileobj(client, bucket, src, key, metadata)

        # StringIO/BytesIO buffer
        elif isinstance(src, (BytesIO, StringIO)) and src_name is not None:
            src = wrap_string(src)
            self._upload_fileobj(client, bucket, src, key, metadata)

        else:
            raise NotImplementedError

    def _get_and_register_artifact(self, src: str, fetch_mode: str) -> str:
        """
        Method to fetch an artifact from the backend an to register
        it on the paths registry.
        """
        client = self._get_client()
        bucket = get_uri_netloc(self.artifact_uri)
        self._check_access_to_storage(client, bucket)
        key = get_uri_path(src)

        self.logger.info(f"Fetching resource {src} from store {self.name}")

        # Return a presigned URL
        if fetch_mode == self.NATIVE:
            url = self._get_presigned_url(client, bucket, key)
            self._register_resource(f"{src}_{fetch_mode}", url)
            return url

        # Get file from remote and store locally
        if fetch_mode == self.FILE:
            obj = self._get_data(client, bucket, key)
            filepath = self._store_data(obj, key)
            self._register_resource(f"{src}_{fetch_mode}", filepath)
            return filepath

        if fetch_mode == self.BUFFER:
            raise NotImplementedError

    def _get_client(self) -> S3Client:
        """
        Return a boto client.
        """
        return boto3.client("s3", **self.config)

    def _check_access_to_storage(self, client: S3Client, bucket: str) -> None:
        """
        Check access to storage.
        """
        try:
            client.head_bucket(Bucket=bucket)
        except ClientError:
            raise StoreError("No access to s3 bucket!")

    @staticmethod
    def _get_presigned_url(client: S3Client, bucket: str, src: str) -> str:
        """
        Encode credentials in S3 URI.
        """
        if src.startswith("/"):
            src = src[1:]
        return client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket, "Key": src},
            ExpiresIn=7200,
        )

    @staticmethod
    def _upload_file(
        client: S3Client, bucket: str, src: str, key: str, metadata: dict
    ) -> None:
        """
        Upload file to S3.
        """
        ex_args = {"Metadata": metadata}
        client.upload_file(Filename=src, Bucket=bucket, Key=key, ExtraArgs=ex_args)

    @staticmethod
    def _upload_fileobj(
        client: S3Client, bucket: str, obj: IO, key: str, metadata: dict
    ) -> None:
        """
        Upload fileobject to S3.
        """
        ex_args = {"Metadata": metadata}
        client.upload_fileobj(obj, Bucket=bucket, Key=key, ExtraArgs=ex_args)

    @staticmethod
    def _get_data(client: S3Client, bucket: str, key: str) -> bytes:
        """
        Download object from S3.
        """
        obj = client.get_object(Bucket=bucket, Key=key)
        return obj["Body"].read()

    def _store_data(self, obj: bytes, key: str) -> str:
        """
        Store data locally in temporary folder and return tmp path.
        """
        check_make_dir(self.temp_dir)
        name = get_name_from_uri(key)
        filepath = get_path(self.temp_dir, name)
        write_bytes(obj, filepath)
        return filepath
