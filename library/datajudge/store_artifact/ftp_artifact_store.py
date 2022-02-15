"""
Implementation of FTP artifact store.
"""
import ftplib
import json
from contextlib import contextmanager
from ftplib import FTP
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any, Optional, Tuple

from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.file_utils import check_path, get_path
from datajudge.utils.io_utils import wrap_string, write_bytesio
from datajudge.utils.uri_utils import (build_key, get_name_from_uri,
                                       get_uri_path, parse_uri)


class FTPArtifactStore(ArtifactStore):
    """
    FTP artifact store object.

    Allows the client to interact with remote FTP store.

    """

    def __init__(self,
                 artifact_uri: str,
                 config: Optional[dict] = None
                 ) -> None:
        super().__init__(artifact_uri, config)
        if self.config is None:
            parsed = parse_uri(self.artifact_uri)
            self.config = {
                "host": "localhost" if parsed.hostname is None
                        else parsed.hostname,
                "port": 21 if parsed.port is None
                        else parsed.port,
                "user": parsed.username,
                "password": parsed.password,
            }

        self.path = parsed.path
        self._check_access_to_storage(self.path)

    def persist_artifact(self,
                         src: Any,
                         dst: str,
                         src_name: str,
                         metadata: Optional[dict] = None
                         ) -> Tuple[str, str]:
        """
        Persist an artifact.
        """
        path = build_key(dst)
        self._check_access_to_storage(path, write=True)

        with self._get_client() as ftp:

            # Change working dir
            ftp.cwd(path)

            # Local file or dump string
            if isinstance(src, (str, Path)) and check_path(src):
                with open(src, "rb") as file:
                    ftp.storbinary("STOR " + src_name, file)

            # Dictionary
            elif isinstance(src, dict) and src_name is not None:
                src = json.dumps(src)
                src = write_bytesio(src)
                ftp.storbinary("STOR " + src_name, src)

            # StringIO/BytesIO buffer
            elif isinstance(src, (BytesIO, StringIO)) and src_name is not None:
                src = wrap_string(src)
                ftp.storbinary("STOR " + src_name, src)

            else:
                raise NotImplementedError

    def fetch_artifact(self, src: str, dst: str) -> str:
        """
        Method to fetch an artifact.
        """
        # Get file from remote (write on BytesIO)
        key = get_uri_path(src)
        bytesio = BytesIO()
        with self._get_client() as ftp:
            ftp.retrbinary("RETR " + key, bytesio.write)
            bytesio.seek(0)
        obj = bytesio.read()

        # Store locally
        self._check_temp_dir(dst)
        name = get_name_from_uri(key)
        filepath = get_path(dst, name)
        self._store_fetched_artifact(obj, filepath)
        return filepath

    # pylint: disable=arguments-differ
    def _check_access_to_storage(self,
                                 dst: str,
                                 write: bool = False) -> None:
        """
        Check if there is access to the storage.
        """
        with self._get_client() as ftp:
            try:
                ftp.cwd(dst)
            except ftplib.error_perm as ex:
                if write:
                    self._mkdir(dst)
                else:
                    raise ex

    # Partial readaptation from mlflow repo on GitHub.
    @contextmanager
    def _get_client(self):
        """
        Yield an FTP client.
        """
        ftp = FTP()
        ftp.connect(self.config["host"], self.config["port"])
        ftp.login(self.config["user"], self.config["password"])
        yield ftp
        ftp.close()

    def _mkdir(self, path):
        """
        Make directory in FTP storage.
        """
        with self._get_client() as ftp:
            try:
                ftp.mkd(path)
                ftp.cwd(path)
            except ftplib.error_perm:
                parent = str(Path(path).parent)
                self._mkdir(parent)
                self._mkdir(path)
