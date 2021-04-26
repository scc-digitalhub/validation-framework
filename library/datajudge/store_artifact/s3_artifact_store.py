import json
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any, Optional

from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.io_utils import wrap_string
from datajudge.utils.s3_utils import (build_s3_key, build_s3_uri,
                                      check_bucket, get_bucket,
                                      get_object, get_s3_path, put_object,
                                      s3_client_creator, upload_file,
                                      upload_fileobj)
from datajudge.utils.uri_utils import check_local_scheme


class S3ArtifactStore(ArtifactStore):
    """
    S3 artifact store object.

    Allows the client to interact with S3 based storages.
    The credentials keys must be the same as the keywords arguments
    of boto3.client() method.

    Attributes
    ----------
    client :
        An S3 client to interact with the storage.

    See also
    --------
    ArtifactStore : Abstract artifact store class.

    """

    def __init__(self,
                 artifact_uri: str,
                 config: Optional[dict] = None,
                 data: bool = False) -> None:
        super().__init__(artifact_uri, config, data)
        self.client = s3_client_creator(**self.config)
        self.bucket = get_bucket(self.artifact_uri)
        self._check_access_to_storage()

    def persist_artifact(self,
                         src: Any,
                         dst: str,
                         src_name: Optional[str] = None) -> None:
        """
        Persist an artifact.
        """
        self._check_access_to_storage(self.bucket)
        key = build_s3_key(dst, src_name)

        # Local file
        if isinstance(src, (str, Path)) and check_local_scheme(src):
            upload_file(self.client, src, self.bucket, key)

        # Dictionary
        elif isinstance(src, dict) and src_name is not None:
            src = json.dumps(src)
            put_object(self.client, src, self.bucket, key)

        # StringIO/BytesIO buffer
        elif isinstance(src, (BytesIO, StringIO)) and src_name is not None:
            src = wrap_string(src)
            upload_fileobj(self.client, src, self.bucket, key)

        else:
            raise NotImplementedError

    def fetch_artifact(self, src: str) -> BytesIO:
        """
        Method to fetch an artifact.
        """
        key = get_s3_path(src)
        return get_object(self.client, self.bucket, key)

    def _check_access_to_storage(self) -> None:
        """
        Check access to storage.
        """
        if not check_bucket(self.client, self.bucket):
            raise RuntimeError("No access to s3 bucket!")

    def get_run_artifacts_uri(self, run_id: str) -> str:
        """
        Return the URI of the artifact store for the Run.
        """
        return build_s3_uri(self.artifact_uri, run_id)
