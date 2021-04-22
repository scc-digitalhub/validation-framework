import json
import os
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any, Optional

from botocore.client import ClientError
from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.io_utils import wrap_string
from datajudge.utils.s3_utils import (build_s3_key, build_s3_uri, get_bucket,
                                      get_obj, get_s3_path, put_object,
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
        self._check_access_to_storage(self.bucket)

    def persist_artifact(self,
                         src: Any,
                         dst: str,
                         src_name: Optional[str] = None) -> None:
        """
        Persist an artifact.
        """
        self._check_access_to_storage(self.bucket)

        local = check_local_scheme(src)
        if local:
            src_name = os.path.basename(src) if src_name is None else src_name

        key = build_s3_key(dst, src_name)

        # Local file
        if isinstance(src, (str, Path)) and local:
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
        return get_obj(self.client, self.bucket, key)

    def _check_access_to_storage(self,
                                 bucket: str) -> None:
        """
        Check access to storage.
        """
        try:
            self.client.head_bucket(Bucket=bucket)
        except ClientError as c_err:
            raise c_err

    def get_run_artifacts_uri(self, run_id: str) -> str:
        """
        Return the URI of the artifact store for the Run.
        """
        return build_s3_uri(self.artifact_uri, run_id)
