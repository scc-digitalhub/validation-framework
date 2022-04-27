"""
Implementation of REST artifact store.
"""
import json
from io import BytesIO, StringIO
from pathlib import Path
from typing import Any, Optional, Tuple

import requests
from requests.models import HTTPError

from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.file_utils import check_make_dir, check_path, get_path
from datajudge.utils.io_utils import write_bytes
from datajudge.utils.rest_utils import api_get_call, api_put_call
from datajudge.utils.uri_utils import check_url, get_name_from_uri, rebuild_uri


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
        self._check_access_to_storage(dst)

        url = check_url(dst)

        kwargs = self._parse_auth({})

        # Local file
        if isinstance(src, (str, Path)) and check_path(src):
            kwargs["data"] = open(src, "rb").read()
            api_put_call(url, **kwargs)

        # Dictionary
        elif isinstance(src, dict) and src_name is not None:
            kwargs["data"] = json.dumps(src)
            api_put_call(url, **kwargs)

        # StringIO/BytesIO buffer
        elif isinstance(src, (BytesIO, StringIO)) and src_name is not None:
            kwargs["data"] = src.read()
            api_put_call(url, **kwargs)

        else:
            raise NotImplementedError

    def fetch_artifact(self,
                       src: str,
                       file_format: str) -> str:
        """
        Method to fetch an artifact.
        """
        self._check_access_to_storage(self.artifact_uri)
        
        key = rebuild_uri(src)
        tmp_path = self.resource_paths.get_resource(key)
        if tmp_path is not None:
            return tmp_path

        # Get file from remote
        kwargs = self._parse_auth({})
        res = api_get_call(key, **kwargs)
        obj = res.content

        # Store locally
        check_make_dir(self.temp_dir)
        name = get_name_from_uri(key)
        filepath = get_path(self.temp_dir, name)
        write_bytes(obj, filepath)
        
        # Register resource on store
        self.resource_paths.register(key, filepath)
        return filepath

    # pylint: disable=arguments-differ
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
                raise HTTPError("Something wrong, response code ",
                                f"{response.status_code} for url ",
                                f"{url}.")
        except Exception as ex:
            raise ex
        
    def _parse_auth(self, kwargs: dict) -> dict:
        """
        Parse auth config.
        """
        if self.config is not None:
            if self.config["auth"] == "basic":
                kwargs["auth"] = self.config["user"], self.config["password"]
            if self.config["auth"] == "oauth":
                kwargs["headers"] = {
                    "Authorization": f"Bearer {self.config['token']}"
                }
        return kwargs
