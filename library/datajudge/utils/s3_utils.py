import urllib.parse
from pathlib import Path
from typing import Type

import boto3
import botocore.client as bc  # type: ignore
from botocore.client import Config


def s3client_creator(s3_endpoint: str,
                     s3_access_key: str,
                     s3_secret_key: str) -> Type["bc.S3"]:
    """
    Return boto client.
    """
    return boto3.client('s3',
                        endpoint_url=s3_endpoint,
                        aws_access_key_id=s3_access_key,
                        aws_secret_access_key=s3_secret_key,
                        config=Config(signature_version='s3v4'),
                        region_name='us-east-1')


def parse_S3_uri(uri: str) -> urllib.parse.ParseResult:
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
    parsed = parse_S3_uri(uri)
    s3_path = str(Path(parsed.path, *args))
    s3_new_url = urllib.parse.urlunparse((parsed.scheme,
                                          parsed.netloc,
                                          s3_path,
                                          parsed.params,
                                          parsed.query,
                                          parsed.fragment))
    return s3_new_url


def build_S3_key(dst: str, src_name: str) -> str:
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
    parsed = parse_S3_uri(uri)
    return parsed.path


def get_bucket(uri: str) -> str:
    """
    Parse an S3 URI, returning bucket.
    """
    parsed = parse_S3_uri(uri)
    return parsed.netloc
