import json
import os
from pathlib import Path
from typing import Any, Optional

from botocore.client import ClientError
from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.s3_utils import (build_S3_key, build_s3_uri, get_bucket,
                                      s3client_creator, split_path_name)


class S3ArtifactStore(ArtifactStore):
    """
    S3 Artifact Store to interact with S3 based storages.
    The credentials must follow the keywords arguments of
    the boto3 client creation method.

    Attributes
    ----------
    client :
        An S3 client to interact with the storage.

    """

    def __init__(self,
                 artifact_uri: str,
                 config: Optional[dict] = None) -> None:
        super().__init__(artifact_uri, config)
        self.client = s3client_creator(**self.config)
        self.bucket = get_bucket(self.artifact_uri)
        self._check_access_to_storage(self.bucket)

    def persist_artifact(self,
                         src: Any,
                         dst: str,
                         src_name: Optional[str] = None) -> None:
        """
        Persist an artifact.
        """
        if isinstance(src, list):
            for obj in src:
                self.persist_artifact(obj, dst, src_name)

        self._check_access_to_storage(self.bucket)

        # src is a local file in this case
        if isinstance(src, (str or Path)) and src_name is None:

            # Check if resource has size > 0
            if Path(src).stat().st_size == 0:
                raise OSError("File is empty, will not be persisted to S3.")

            src_name = os.path.basename(src)
            key = build_S3_key(dst, src_name)
            self.client.upload_file(Filename=src,
                                    Bucket=self.bucket,
                                    Key=key)

        # or a dictionary that we dump in a json
        elif isinstance(src, dict) and src_name is not None:

            json_obj = json.dumps(src)
            key = build_S3_key(dst, src_name)
            self.client.put_object(Body=json_obj,
                                   Bucket=self.bucket,
                                   Key=key)

        return split_path_name(dst)

    def _check_access_to_storage(self,
                                 bucket: str) -> None:
        """
        Check access to storage.
        """
        try:
            self.client.head_bucket(Bucket=bucket)
        except ClientError:
            raise BaseException("The bucket does not exist or" +
                                " you have no access to it.")

    def get_run_artifacts_uri(self, run_id: str) -> str:
        """
        Return the URI of the artifact store for the Run.
        """
        return build_s3_uri(self.artifact_uri, run_id)
