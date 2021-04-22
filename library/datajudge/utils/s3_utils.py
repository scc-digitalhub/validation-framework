"""
Common S3 utils.
"""
# pylint: disable=invalid-name,import-error,unused-import
import urllib.parse
from io import BytesIO
from pathlib import Path
from typing import Any, Tuple, Type

import boto3
import botocore.client as bc
from botocore.client import Config


s3_client = Type["bc.S3"]


def s3_client_creator(**kwargs) -> s3_client:
    """
    Return boto client.
    """
    try:
        return boto3.client('s3',
                            config=Config(signature_version='s3v4'),
                            region_name='us-east-1',
                            **kwargs)
    except Exception as ex:
        raise ex


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


def split_path_name(uri: str) -> Tuple[str, str]:
    """
    Return uri and key.
    """
    key = get_s3_path(uri)
    # orrendo
    base_uri = "s3://" + get_bucket(uri)
    return key, base_uri


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
                key: str) -> None:
    """
    Upload file to S3.
    """
    client.upload_file(Filename=src,
                       Bucket=bucket,
                       Key=key)


def put_object(client: s3_client,
               obj: str,
               bucket: str,
               key: str) -> None:
    """
    Upload json to S3.
    """
    client.put_object(Body=obj,
                      Bucket=bucket,
                      Key=key)


def upload_fileobj(client: s3_client,
                   obj: BytesIO,
                   bucket: str,
                   key: str) -> None:
    """
    Upload fileobject to S3.
    """
    client.upload_fileobj(obj,
                          Bucket=bucket,
                          Key=key)


def get_obj(client: s3_client,
            bucket: str,
            key: str) -> None:
    """
    Download object from S3 into a buffer.
    """
    obj = client.get_object(Bucket=bucket, Key=key)
    buff = BytesIO()
    buff.write(obj['Body'].read())
    buff.seek(0)
    return buff
