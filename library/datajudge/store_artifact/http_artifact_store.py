"""
Implementation of REST artifact store.
"""
from typing import Any, Optional, Tuple

import requests
from requests.models import HTTPError

from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.file_utils import check_make_dir, get_path
from datajudge.utils.io_utils import write_bytes
from datajudge.utils.uri_utils import get_name_from_uri, rebuild_uri


class HTTPArtifactStore(ArtifactStore):
    """
    Rest artifact store object.

    Allows the client to interact with remote HTTP store.

    """

    def __init__(self,
                 artifact_uri: str,
                 temp_dir: str,
                 config: Optional[dict] = None
                 ) -> None:
        super().__init__(artifact_uri, temp_dir, config)

    def persist_artifact(self,
                         src: Any,
                         dst: str,
                         src_name: str,
                         metadata: dict
                         ) -> Tuple[str, str]:
        """
        Persist an artifact.
        """
        raise NotImplementedError

    def _get_and_register_artifact(self,
                                   src: str,
                                   file_format: str) -> str:
        """
        Method to fetch an artifact from the backend an to register
        it on the paths registry.
        """
        self._check_access_to_storage(self.artifact_uri)
        key = rebuild_uri(src)

        # Get file from remote
        obj = self._get_data(key)

        # Store locally
        filepath = self._store_data(obj, key)

        # Register resource on store
        self._register_resource(f"{src}_{file_format}", filepath)
        return filepath


    def _check_access_to_storage(self, dst: str) -> None:
        """
        Check if there is access to the storage.
        """
        try:
            self._check_url_availability(dst)
        except Exception as ex:
            raise ex

    @staticmethod
    def _check_url_availability(url: str) -> None:
        """
        Check URL availability.
        """
        try:
            response = requests.head(url)
            if not response.ok:
                raise HTTPError("Something wrong, response code " +
                                f"{response.status_code} for url " +
                                f"{url}.")
        except Exception as ex:
            raise ex

    def _parse_auth(self) -> dict:
        """
        Parse auth config.
        """
        kwargs = {}
        if self.config is not None:
            if self.config["auth"] == "basic":
                kwargs["auth"] = self.config["user"], self.config["password"]
            if self.config["auth"] == "oauth":
                kwargs["headers"] = {
                    "Authorization": f"Bearer {self.config['token']}"
                }
        return kwargs

    def _get_data(self, key: str) -> bytes:
        """
        Get data from remote.
        """
        kwargs = self._parse_auth()
        res = requests.get(key, **kwargs)
        return res.content

    def _store_data(self,
                    obj: bytes,
                    key: str) -> str:
        """
        Store data locally in temporary folder and return tmp path.
        """
        check_make_dir(self.temp_dir)
        name = get_name_from_uri(key)
        filepath = get_path(self.temp_dir, name)
        write_bytes(obj, filepath)
        return filepath
