"""
Common S3 utils.
"""
# pylint: disable=invalid-name
from typing import IO

from datajudge.utils.typing import s3_client


def check_bucket(client: s3_client, bucket: str) -> bool:
    """
    Check access to a bucket.
    """
    try:
        client.head_bucket(Bucket=bucket)
        return True
    except Exception:
        return False


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


def upload_fileobj(client: s3_client,
                   obj: IO,
                   bucket: str,
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


def get_object(client: s3_client,
               bucket: str,
               key: str) -> None:
    """
    Download object from S3.
    """
    obj = client.get_object(Bucket=bucket, Key=key)
    return obj['Body'].read()
