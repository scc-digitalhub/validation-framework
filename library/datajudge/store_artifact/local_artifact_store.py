"""
Implementation of local artifact store.
"""
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any, Optional

from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.file_utils import (check_dir, copy_file, get_path,
                                        make_dir, write_json, write_object)
from datajudge.utils.uri_utils import check_local_scheme


class LocalArtifactStore(ArtifactStore):
    """
    Local artifact store object.

    Allows the client to interact with local filesystem.

    See also
    --------
    ArtifactStore : Abstract artifact store class.

    """

    def __init__(self,
                 artifact_uri: str,
                 config: Optional[dict] = None,
                 data: bool = False) -> None:
        super().__init__(artifact_uri, config, data)
        self._check_access_to_storage(self.artifact_uri)

    def persist_artifact(self,
                         src: Any,
                         dst: str,
                         src_name: Optional[str] = None
                         ) -> None:
        """
        Persist an artifact.
        """
        self._check_access_to_storage(dst)

        if src_name is not None:
            dst = get_path(dst, src_name)

        # Local file
        if isinstance(src, (str, Path)):
            if check_local_scheme(src):
                copy_file(src, dst)
            else:
                raise OSError("Not a local file!")

        # Dictionary
        elif isinstance(src, dict) and src_name is not None:
            write_json(src, dst)

        # StringIO/BytesIO buffer
        elif isinstance(src, (BytesIO, StringIO)) and src_name is not None:
            write_object(src, dst)

        else:
            raise NotImplementedError

    def fetch_artifact(self, src: str, dst: str) -> str:
        """
        Method to fetch an artifact.
        For this store, simply returns original file
        positions.
        """
        self._check_temp_dir(dst)
        return src

    def _check_access_to_storage(self, dst: str) -> None: # pylint: disable=arguments-differ
        """
        Check if there is access to the storage.
        """
        if not self.data and not check_dir(dst):
            make_dir(dst)

    def get_run_artifacts_uri(self, run_id: str) -> str:
        """
        Return the path of the artifact store for the Run.
        """
        return get_path(self.artifact_uri, run_id)
