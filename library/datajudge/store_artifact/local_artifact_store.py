"""
LocalArtifactStore module.
"""
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any

from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.file_utils import (
    check_dir,
    check_path,
    copy_file,
    get_path,
    make_dir,
)
from datajudge.utils.io_utils import write_json, write_object


class LocalArtifactStore(ArtifactStore):
    """
    Implementation of a local artifact store object that allows the user to
    interact with the local filesystem.
    """

    def persist_artifact(self, src: Any, dst: str, src_name: str, *args) -> None:
        """
        Method to persist an artifact.

        Parameters
        ----------
        src : Any
            The source file to be persisted.
        dst : str
            Destination folder.
        src_name : str
            Name given to the source file.

        Returns
        -------
        None

        Raises
        ------
        NotImplementedError
            If the object located in 'src' is not one of the accepted types.
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
            raise NotImplementedError(
                "Invalid object type located at src, it could not be persisted."
            )

    def _get_and_register_artifact(self, src: str, fetch_mode: str) -> str:
        """
        Method to fetch an artifact from the backend and to register it on the paths registry.

        Parameters:
        -----------
        src: str
            The name of the file.
        fetch_mode: str
            Whether the fetch mode is NATIVE or FILE.

        Returns:
        --------
        str:
            The location of the requested file.

        Raises:
        -------
        NotImplementedError:
            If the user tries to use a 'fetch_mode' that is not implemented yet.
        """
        self.logger.info(f"Fetching resource {src} from store {self.name}")

        # Return file location on filesystem
        if fetch_mode == self.NATIVE:
            self._register_resource(f"{src}_{fetch_mode}", src)
            return src

        # Return file location on filesystem
        if fetch_mode == self.FILE:
            self._register_resource(f"{src}_{fetch_mode}", src)
            return src

        if fetch_mode == self.BUFFER:
            raise NotImplementedError(
                "File fetch using buffers is not yet implemented."
            )

    def _check_access_to_storage(self, dst: str, write: bool = False) -> None:
        """
        Check if there is access to the path.

        Parameters
        ----------
        dst : str
            The path being checked.
        write : bool, optional
            Whether we want to check for writing permission. Default is False.

        Returns
        -------
        None
        """
        if write and not check_dir(dst):
            make_dir(dst)

    def _get_data(self, *args) -> None:
        """
        Placeholder method.

        Returns:
        --------
        None
        """
        ...

    def _store_data(self, *args) -> None:
        """
        Placeholder method.

        Returns:
        --------
        None
        """
        ...
