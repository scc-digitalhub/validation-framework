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
        Persist an artifact on S3 based storage.

        Parameters:
        -----------
        src : Any
            The source object to be persisted. It can be a file path as a string or Path object,
            a dictionary containing key-value pairs, or a buffer like StringIO/BytesIO.

        dst : str
            The destination partition for the artifact.

        src_name : str
            The name of the source object.

        metadata : dict
            Additional information to be stored with the artifact.

        Raises:
        -------
        NotImplementedError :
            If the source object is not a file path, dictionary, StringIO/BytesIO buffer.

        Returns:
        --------
        None
        """
        client = self._get_client()
        bucket = get_uri_netloc(self.artifact_uri)
        self._check_access_to_storage(client, bucket)

        # Build the key for the artifact
        key = build_key(dst, src_name)

        # Local file
        if isinstance(src, (str, Path)) and check_path(src):
            self._upload_file(client, bucket, str(src), key, metadata)

        # Dictionary
        elif isinstance(src, dict) and src_name is not None:
            # Convert the dictionary to JSON string and write it to BytesIO buffer
            src = json.dumps(src)
            src = write_bytesio(src)
            self._upload_fileobj(client, bucket, src, key, metadata)

        # StringIO/BytesIO buffer
        elif isinstance(src, (BytesIO, StringIO)) and src_name is not None:
            # Wrap the buffer in a BufferedIOBase object and upload it
            src = wrap_string(src)
            self._upload_fileobj(client, bucket, src, key, metadata)

        else:
            raise NotImplementedError

    def _get_and_register_artifact(self, src: str, fetch_mode: str) -> str:
        """
        Method to fetch an artifact from the backend and to register it on the paths registry.

        Parameters:
        -----------
        src : str
            The source location of the artifact.

        fetch_mode : str
            The mode for fetching the artifact. It can be one of the following:
                * self.NATIVE : Returns a presigned URL.
                * self.FILE : Gets the file from remote and stores it locally.
                * self.BUFFER : Not implemented.

        Raises:
        -------
        NotImplementedError :
            If fetch_mode is not one of the supported modes.

        Returns:
        --------
        str
            Returns a presigned URL (if fetch_mode is self.NATIVE) or the file path (if fetch_mode is self.FILE).
        """
        client = self._get_client()
        bucket = get_uri_netloc(self.artifact_uri)
        self._check_access_to_storage(client, bucket)
        key = get_uri_path(src)

        # Log the information about the resource being fetched
        self.logger.info(f"Fetching resource {src} from store {self.name}")

        # Return a presigned URL
        if fetch_mode == self.NATIVE:
            url = self._get_presigned_url(client, bucket, key)
            self._register_resource(f"{src}_{fetch_mode}", url)
            return url

        # Get the file from S3 and save it locally
        elif fetch_mode == self.FILE:
            obj = self._get_data(client, bucket, key)
            filepath = self._store_data(obj, key)
            self._register_resource(f"{src}_{fetch_mode}", filepath)
            return filepath

        elif fetch_mode == self.BUFFER:
            raise NotImplementedError

        else:
            raise NotImplementedError

    def _get_client(self) -> S3Client:
        """
        Return a boto client.

        Returns:
        --------
        S3Client
            Returns a client object that interacts with the S3 storage service.
        """
        return boto3.client("s3", **self.config)

    def _check_access_to_storage(self, client: S3Client, bucket: str) -> None:
        """
        Check if the S3 bucket is accessible by sending a head_bucket request.

        Parameters:
        -----------
        client: S3Client
            An instance of 'S3Client' class that provides client interfaces to S3 service.
        bucket: string
            A string representing the name of the S3 bucket for which access needs to be checked.

        Returns:
        --------
        None

        Raises:
        -------
        StoreError:
            If access to the specified bucket is not available.

        """
        try:
            client.head_bucket(Bucket=bucket)
        except ClientError:
            raise StoreError("No access to s3 bucket!")

    @staticmethod
    def _get_presigned_url(client: S3Client, bucket: str, src: str) -> str:
        """
        Returns a presigned URL for a specified object in an S3 bucket.

        Parameters:
        -----------
        client: S3Client
            An instance of 'S3Client' class that provides client interfaces to S3 service.
        bucket: string
            A string representing the name of the S3 bucket containing the object.
        src: string
            A string representing the key of the object.

        Returns:
        --------
        url: string
            A string representing the generated Presigned URL

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

        Parameters
        ----------
        client : S3Client
            An instance of the S3 Client used for uploading the file.
        bucket : str
            The name of the S3 bucket where the file will be uploaded.
        src : str
            The path to the file that needs to be uploaded to S3.
        key : str
            The key under which the file needs to be saved in S3.
        metadata : dict
            A dictionary containing metadata to be associated with the uploaded object.

        Returns
        -------
        None
        """
        ex_args = {"Metadata": metadata}
        client.upload_file(Filename=src, Bucket=bucket, Key=key, ExtraArgs=ex_args)

    @staticmethod
    def _upload_fileobj(
        client: S3Client, bucket: str, obj: IO, key: str, metadata: dict
    ) -> None:
        """
        Upload a file object to S3.

        Parameters
        ----------
        client : S3Client
            An instance of the S3 Client used for uploading the file object.
        bucket : str
            The name of the S3 bucket where the file object will be uploaded.
        obj : io.IOBase
            A file object representing the data to be uploaded to S3.
        key : str
            The key under which the file object needs to be saved in S3.
        metadata : dict
            A dictionary containing metadata to be associated with the uploaded object.

        Returns
        -------
        None
        """
        ex_args = {"Metadata": metadata}
        client.upload_fileobj(obj, Bucket=bucket, Key=key, ExtraArgs=ex_args)

    @staticmethod
    def _get_data(client: S3Client, bucket: str, key: str) -> bytes:
        """
        Download an object from S3.

        Parameters
        ----------
        client : S3Client
            An instance of the S3 Client used for downloading the object.
        bucket : str
            The name of the S3 bucket where the object resides.
        key : str
            The key under which the object is stored in the specified bucket.

        Returns
        -------
        bytes
            A bytes object representing the downloaded object.

        """
        obj = client.get_object(Bucket=bucket, Key=key)
        return obj["Body"].read()

    def _store_data(self, obj: bytes, key: str) -> str:
        """
        Store binary data in a temporary directory and return the file path.

        Parameters
        ----------
        obj : bytes
            Binary data to store in a temporary directory.
        key : str
            Key of the S3 object to store.

        Returns
        -------
        str
            Path of the stored data file.
        """
        check_make_dir(self.temp_dir)
        name = get_name_from_uri(key)
        filepath = get_path(self.temp_dir, name)
        write_bytes(obj, filepath)
        return filepath
