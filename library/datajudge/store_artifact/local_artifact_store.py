from pathlib import Path
from typing import Any, Optional, Tuple

from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.file_utils import (check_dir, check_file_dimension,
                                        copy_file, get_path, make_dir,
                                        write_json, split_path_name)


class LocalArtifactStore(ArtifactStore):
    """
    Local Artifact Store to interact with local filesystem.

    """

    def __init__(self,
                 artifact_uri: str,
                 credentials: Optional[dict] = None) -> None:
        super().__init__(artifact_uri, credentials)

    def persist_artifact(self,
                         src: Any,
                         dst: str,
                         src_name: Optional[str] = None
                         ) -> Tuple[str, str]:
        """
        Persist an artifact and return filename and URI.
        """
        # Check if the destination folder exists
        if isinstance(src, list):
            for obj in src:
                self.persist_artifact(obj, dst, src_name)

        self._check_access_to_storage(dst)

        if src_name is not None:
            dst = get_path(dst, src_name)

        if isinstance(src, dict):
            if src_name is not None:
                write_json(src, dst)
            else:
                raise OSError("File name needed.")

        if isinstance(src, (str, Path)):
            if check_file_dimension(src) > 0:
                copy_file(src, dst)

        return split_path_name(dst)

    @staticmethod
    def _check_access_to_storage(dst) -> None:
        """
        Check if there is access to the storage.
        """
        if not check_dir(dst):
            make_dir(dst)

    def get_run_artifacts_uri(self, run_id: str) -> str:
        """
        Return the path of the artifact store for the Run.
        """
        return get_path(self.artifact_uri, run_id)
