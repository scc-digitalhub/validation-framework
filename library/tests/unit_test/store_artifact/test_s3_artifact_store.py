from pathlib import Path

import pytest
from botocore.exceptions import ClientError

from datajudge.utils.commons import (
    DATAREADER_BUFFER,
    DATAREADER_FILE,
    DATAREADER_NATIVE,
)
from datajudge.utils.exceptions import StoreError
from datajudge.utils.file_utils import get_path
from datajudge.utils.uri_utils import build_key, get_name_from_uri
from tests.conftest import S3_BUCKET, S3_FILENAME, TEST_FILENAME


class TestS3ArtifactStore:
    def test_persist_artifact(
        self, store, temp_file, stringio, bytesio, dictionary, s3
    ):
        dst = "artifact/test/test/"
        src_name = "persist.txt"
        key = build_key(dst, src_name)

        # Local file
        not_exists(s3, key)
        store.persist_artifact(temp_file, dst, src_name, {})
        exists(s3, key)

        # StringIO/
        not_exists(s3, key)
        store.persist_artifact(stringio, dst, src_name, {})
        exists(s3, key)

        # BytesIO
        not_exists(s3, key)
        store.persist_artifact(bytesio, dst, src_name, {})
        exists(s3, key)

        # Dictionary
        not_exists(s3, key)
        store.persist_artifact(dictionary, dst, src_name, {})
        exists(s3, key)

        # Other
        not_exists(s3, key)
        with pytest.raises(NotImplementedError):
            store.persist_artifact(None, dst, src_name, {})
        with pytest.raises(TypeError):
            store.persist_artifact(dictionary, dst, None, {})

    def test_fetch_file(self, store):
        filepath = store.fetch_file(S3_FILENAME)
        assert Path(filepath).is_file()

    def test_fetch_native(self, store):
        string = store.fetch_native(S3_FILENAME)
        assert string.startswith(f"https://test.s3.amazonaws.com/{S3_FILENAME}?")
        assert "AWSAccessKeyId=" in string
        assert "Signature=" in string
        assert "Expires=" in string

    def test_fetch_buffer(self, store):
        with pytest.raises(NotImplementedError):
            store.fetch_buffer(S3_FILENAME)

    def test_get_and_register_artifact(self, store):
        # File
        res = store._get_and_register_artifact(S3_FILENAME, DATAREADER_FILE)
        assert Path(res).is_file()

        # Native
        res = store._get_and_register_artifact(S3_FILENAME, DATAREADER_NATIVE)
        assert res.startswith(f"https://test.s3.amazonaws.com/{S3_FILENAME}?")
        assert "AWSAccessKeyId=" in res
        assert "Signature=" in res
        assert "Expires=" in res

        # Buffer
        with pytest.raises(NotImplementedError):
            store._get_and_register_artifact(S3_FILENAME, DATAREADER_BUFFER)

    def test_check_access_to_storage(self, store, client):
        assert store._check_access_to_storage(client, S3_BUCKET) is None
        with pytest.raises(StoreError):
            store._check_access_to_storage(client, "non-existent-bucket")

    @pytest.mark.parametrize(
        "key", [("artifact/test/persist.txt"), ("/test/test/persist.txt")]
    )
    def test_get_presigned_url(self, store, client, key):
        url = store._get_presigned_url(client, S3_BUCKET, key)
        if key.startswith("/"):
            key = key[1:]
        assert url.startswith(f"https://test.s3.amazonaws.com/{key}?")
        assert "AWSAccessKeyId=" in url
        assert "Signature=" in url
        assert "Expires=" in url

    def test_upload_file(self, store, client, temp_file):
        key = build_key("test", temp_file)
        store._upload_file(client, S3_BUCKET, str(temp_file), key, {})
        assert client.head_object(Bucket=S3_BUCKET, Key=key)

    def test_upload_fileobj(self, store, client, bytesio):
        key = build_key("test", TEST_FILENAME)
        store._upload_fileobj(client, S3_BUCKET, bytesio, key, {})
        assert client.head_object(Bucket=S3_BUCKET, Key=key)

    def test_get_data(self, store, client, bytesio):
        key = build_key("test", TEST_FILENAME)
        store._upload_fileobj(client, S3_BUCKET, bytesio, key, {})
        assert client.head_object(Bucket=S3_BUCKET, Key=key)
        data = store._get_data(client, S3_BUCKET, key)
        assert data == b"test"

    def test_store_data(self, store):
        key = build_key("test", TEST_FILENAME)
        name = get_name_from_uri("s3://" + key)
        filepath = get_path(store.temp_dir, name)
        tmp = store._store_data(b"test", filepath)
        assert Path(tmp).is_file()
        assert Path(tmp).read_bytes() == b"test"
        Path(tmp).unlink()


@pytest.fixture
def store_cfg(s3_store_cfg):
    return s3_store_cfg


# Pathced to return mock client
@pytest.fixture
def store(store, monkeypatch, s3):
    def _get_client(*args, **kwargs):
        return s3

    monkeypatch.setattr(store, "_get_client", _get_client)
    return store


# Quick patched client
@pytest.fixture
def client(store):
    return store._get_client()


def exists(s3, key):
    assert s3.head_object(Bucket=S3_BUCKET, Key=key)
    s3.delete_object(Bucket=S3_BUCKET, Key=key)


def not_exists(s3, key):
    with pytest.raises(ClientError):
        s3.head_object(Bucket=S3_BUCKET, Key=key)
