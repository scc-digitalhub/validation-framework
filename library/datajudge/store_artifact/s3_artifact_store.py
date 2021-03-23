import json
import os
from pathlib import Path
from typing import Any, Optional

from botocore.client import ClientError
from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.s3_utils import (build_S3_key, build_s3_uri, get_bucket,
                                      s3client_creator)


class S3ArtifactStore(ArtifactStore):

    def __init__(self,
                 artifact_uri: str,
                 credentials: Optional[dict] = None) -> None:
        super().__init__(artifact_uri, credentials)
        self.client = s3client_creator(self.credentials["s3_endpoint"],
                                       self.credentials["s3_access_key"],
                                       self.credentials["s3_secret_key"])

    def persist_artifact(self,
                         src: Any,
                         dst: str,
                         src_name: Optional[str] = None) -> None:
        """Persist an artifact."""
        
        if isinstance(src, list):
            for obj in src:
                self.persist_artifact(obj, dst, src_name)

        bucket = get_bucket(dst)
        self._check_access_to_storage(bucket)

        # src is a local file in this case
        if isinstance(src, (str or Path)) and src_name is None:

            # Check if resource has size > 0
            if Path(src).stat().st_size == 0:
                raise OSError("File is empty, will not be logged to S3.")

            src_name = os.path.basename(src)
            key = build_S3_key(dst, src_name)
            self.client.upload_file(Filename=src,
                                    Bucket=bucket,
                                    Key=key)

        # or a dictionary that we dump in a json
        elif isinstance(src, dict) and src_name is not None:
            
            json_obj = json.dumps(src)
            key = build_S3_key(dst, src_name)
            self.client.put_object(Body=json_obj,
                                   Bucket=bucket,
                                   Key=key)

    def _check_access_to_storage(self,
                                 bucket: str) -> None:
        """Check bucket existence."""
        try:
            self.client.head_bucket(Bucket=bucket)
        except ClientError:
            raise BaseException("The bucket does not exist or",
                                " you have no access.")

    def get_run_artifacts_uri(self, run_id: str) -> str:
        """Return the URI of the artifact store for the Run."""
        return build_s3_uri(self.artifact_uri, run_id)
