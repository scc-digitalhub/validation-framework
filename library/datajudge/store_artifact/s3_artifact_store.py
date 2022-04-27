"""
Implementation of S3 artifact store.
"""
# pylint: disable=import-error
import json
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any, IO, Optional, Type

import boto3
import botocore.client
from botocore.exceptions import ClientError

from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.exceptions import StoreError
from datajudge.utils.file_utils import check_make_dir, check_path, get_path
from datajudge.utils.io_utils import wrap_string, write_bytes, write_bytesio
from datajudge.utils.uri_utils import (build_key, get_name_from_uri,
                                       get_uri_netloc, get_uri_path)


s3_client = Type["botocore.client.S3"]


class S3ArtifactStore(ArtifactStore):
    """
    S3 artifact store object.

    Allows the client to interact with S3 based storages.

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
        client = self._get_client()
        bucket = get_uri_netloc(self.artifact_uri)
        self._check_access_to_storage(client, bucket)

        key = build_key(dst, src_name)

        # Local file
        if isinstance(src, (str, Path)) and check_path(src):
            self._upload_file(client, bucket, src, key, metadata)

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

    def fetch_artifact(self, src: str, file_format: str) -> str:
        """
        Method to fetch an artifact.
        """
        client = self._get_client()
        bucket = get_uri_netloc(self.artifact_uri)
        self._check_access_to_storage(client, bucket)

        if format == "s3":
            return self._build_encoded_s3_path(client, src)

        key = get_uri_path(src)

        tmp_path = self.resource_paths.get_resource(key)
        if tmp_path is not None:
            return tmp_path

        # Get file from remote
        obj = self._get_object(client, bucket, key)

        # Store locally
        check_make_dir(self.temp_dir)
        name = get_name_from_uri(key)
        filepath = get_path(self.temp_dir, name)
        write_bytes(obj, filepath)

        # Register resource on store
        self.resource_paths.register(key, filepath)
        return filepath

    def _get_client(self) -> s3_client:
        """
        Return a boto client.
        """
        return boto3.client("s3", **self.config)

    def _check_access_to_storage(self,
                                 client: s3_client,
                                 bucket: str) -> None:
        """
        Check access to storage.
        """
        try:
            client.head_bucket(Bucket=bucket)
        except ClientError:
            raise StoreError("No access to s3 bucket!")

    def _build_encoded_s3_path(self,
                               client: s3_client,
                               bucket: str,
                               src: str) -> str:
        """
        Encode credentials in S3 URI.
        """
        return client.generate_presigned_url(
                    ClientMethod="get_object",
                    Params={"Bucket": bucket,
                            "Key": src},
                    ExpiresIn=7200)

    def _upload_file(self,
                     client: s3_client,
                     bucket: str,
                     src: str,
                     key: str,
                     metadata: dict
                     ) -> None:
        """
        Upload file to S3.
        """
        ex_args = {"Metadata": metadata}
        client.upload_file(Filename=src,
                                Bucket=bucket,
                                Key=key,
                                ExtraArgs=ex_args)

    def _upload_fileobj(self,
                        client: s3_client,
                        bucket: str,
                        obj: IO,
                        key: str,
                        metadata: dict
                        ) -> None:
        """
        Upload fileobject to S3.
        """
        ex_args = {"Metadata": metadata}
        client.upload_fileobj(obj,
                              Bucket=bucket,
                              Key=key,
                              ExtraArgs=ex_args)

    def _get_object(self,
                    client: s3_client,
                    bucket: str,
                    key: str) -> bytes:
        """
        Download object from S3.
        """
        obj = client.get_object(Bucket=bucket,
                                Key=key)
        return obj['Body'].read()
