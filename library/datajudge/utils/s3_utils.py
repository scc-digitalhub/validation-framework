"""
Common S3 utils.
"""
# pylint: disable=invalid-name,import-error,unused-import
import urllib.parse
from pathlib import Path
from typing import Any, IO, Type

import boto3
import botocore.client as bc
from botocore.client import Config


s3_client = Type["bc.S3"]


def s3_client_creator(**kwargs) -> s3_client:
    """
    Return boto client.
    """
    return boto3.client('s3',
                        config=Config(signature_version='s3v4'),
                        region_name='us-east-1',
                        **kwargs)


def parse_s3_uri(uri: str) -> urllib.parse.ParseResult:
    """
    Return parsed URI.
    """
    parsed = urllib.parse.urlparse(uri)
    if parsed.scheme != "s3":
        raise Exception("Not an S3 URI: %s" % uri)
    return parsed


def build_s3_uri(uri: str, *args) -> str:
    """
    Return a full S3 path.
    """
    parsed = parse_s3_uri(uri)
    s3_path = str(Path(parsed.path, *args))
    s3_new_url = urllib.parse.urlunparse((parsed.scheme,
                                          parsed.netloc,
                                          s3_path,
                                          parsed.params,
                                          parsed.query,
                                          parsed.fragment))
    return s3_new_url


def build_s3_key(dst: str, src_name: str) -> str:
    """
    Build key to upload objects.
    """
    key = get_s3_path(dst) + "/" + src_name
    if key.startswith("/"):
        key = key[1:]
    return key


def get_s3_path(uri: str) -> str:
    """
    Return the path portion of S3 URI.
    """
    parsed = parse_s3_uri(uri)
    return parsed.path


def get_bucket(uri: str) -> str:
    """
    Parse an S3 URI, returning bucket.
    """
    parsed = parse_s3_uri(uri)
    return parsed.netloc


def check_bucket(client: s3_client, bucket: str) -> bool:
    """
    Check access to a bucket.
    """
    try:
        client.head_bucket(Bucket=bucket)
        return True
    except Exception:
        raise
        return False


def get_size(src: Any) -> None:
    """
    Check input file size to avoid to upload empty files on S3.
    """
    err_msg = "File is empty, will not be persisted to S3."
    if isinstance(src, (str, Path)):
        if Path(src).stat().st_size == 0:
            raise BaseException(err_msg)


def upload_file(client: s3_client,
                src: str,
                bucket: str,
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


def put_object(client: s3_client,
               obj: str,
               bucket: str,
               key: str,
               metadata: dict
               ) -> None:
    """
    Upload json to S3.
    """
    client.put_object(Body=obj,
                      Bucket=bucket,
                      Key=key,
                      Metadata=metadata)


def upload_fileobj(client: s3_client,
                   obj: IO,
                   bucket: str,
                   key: str,
                   metadata: dict
                   ) -> None:
    """
    Upload fileobject to S3.
    """
    client.upload_fileobj(obj,
                          Bucket=bucket,
                          Key=key,
                          Metadata=metadata)


def get_object(client: s3_client,
               bucket: str,
               key: str) -> None:
    """
    Download object from S3.
    """
    obj = client.get_object(Bucket=bucket, Key=key)
    return obj['Body'].read()
