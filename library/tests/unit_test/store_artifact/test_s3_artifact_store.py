import pytest
from botocore.exceptions import ClientError

from datajudge.utils.commons import (
    DATAREADER_BUFFER,
    DATAREADER_FILE,
    DATAREADER_NATIVE,
)
from datajudge.utils.uri_utils import (
    build_key,
)
from tests.conftest import (S3_BUCKET)


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


class TestS3ArtifactStore:

    def test_persist_artifact(
        self, store, temp_file, stringio, bytesio, dictionary, s3
    ):
        dst = "artifact/test/test/"
        src_name = "persist.txt"
        metadata = {}

        key = build_key(dst, src_name)

        # Local file
        with pytest.raises(ClientError):
            s3.head_object(Bucket=S3_BUCKET, Key=key)
        store.persist_artifact(temp_file, dst, src_name, metadata)
        assert s3.head_object(Bucket=S3_BUCKET, Key=key)
        s3.delete_object(Bucket=S3_BUCKET, Key=key)

        # StringIO/
        with pytest.raises(ClientError):
            s3.head_object(Bucket=S3_BUCKET, Key=key)
        store.persist_artifact(stringio, dst, src_name, metadata)
        assert s3.head_object(Bucket=S3_BUCKET, Key=key)
        s3.delete_object(Bucket=S3_BUCKET, Key=key)

        # BytesIO
        with pytest.raises(ClientError):
            s3.head_object(Bucket=S3_BUCKET, Key=key)
        store.persist_artifact(bytesio, dst, src_name, metadata)
        assert s3.head_object(Bucket=S3_BUCKET, Key=key)
        s3.delete_object(Bucket=S3_BUCKET, Key=key)

        # Dictionary
        with pytest.raises(ClientError):
            s3.head_object(Bucket=S3_BUCKET, Key=key)
        store.persist_artifact(dictionary, dst, src_name, metadata)
        assert s3.head_object(Bucket=S3_BUCKET, Key=key)
        s3.delete_object(Bucket=S3_BUCKET, Key=key)

        # Other
        with pytest.raises(ClientError):
            s3.head_object(Bucket=S3_BUCKET, Key=key)
        with pytest.raises(NotImplementedError):
            store.persist_artifact(None, dst, src_name, metadata)
        with pytest.raises(TypeError):
            store.persist_artifact(dictionary, dst, None, metadata)
