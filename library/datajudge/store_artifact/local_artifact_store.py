"""
Implementation of local artifact store.
"""
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any, Optional

from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.file_utils import (check_dir, check_make_dir, check_path, copy_file,
                                        get_path, make_dir)
from datajudge.utils.io_utils import write_json, write_object


write_object

class LocalArtifactStore(ArtifactStore):
    """
    Local artifact store object.

    Allows the client to interact with local filesystem.

    """

    def __init__(self,
                 artifact_uri: str,
                 config: Optional[dict] = None
                 ) -> None:
        super().__init__(artifact_uri, config)
        self._check_access_to_storage(self.artifact_uri)

    def persist_artifact(self,
                         src: Any,
                         dst: str,
                         src_name: str,
                         metadata: dict
                         ) -> None:
        """
        Persist an artifact.
        """
        self._check_access_to_storage(dst, write=True)

        if src_name is not None:
            dst = get_path(dst, src_name)

        # Local file or dump string
        if isinstance(src, (str, Path)) and check_path(src):
            copy_file(src, dst)

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
        check_make_dir(dst)
        return src

    # pylint: disable=arguments-differ
    def _check_access_to_storage(self,
                                 dst: str,
                                 write: bool = False) -> None:
        """
        Check if there is access to the storage.
        """
        if write and not check_dir(dst):
            make_dir(dst)
