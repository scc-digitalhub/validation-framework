"""
Implementation of REST artifact store.
"""
import json
from io import BytesIO, StringIO
from pathlib import Path
from typing import IO, Any, Optional, Tuple, Union

from datajudge.store_artifact.artifact_store import ArtifactStore
from datajudge.utils.file_utils import check_path, get_path
from datajudge.utils.rest_utils import (api_get_call, api_put_call,
                                        check_url_availability)
from datajudge.utils.uri_utils import check_url, get_name_from_uri, rebuild_uri


class HTTPArtifactStore(ArtifactStore):
    """
    Rest artifact store object.

    Allows the client to interact with remote HTTP store.

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
                         src_name: str,
                         metadata: dict
                         ) -> Tuple[str, str]:
        """
        Persist an artifact.
        """
        self._check_access_to_storage(dst)

        url = check_url(dst)

        kwargs = {
            "auth": self._parse_auth()
        }

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

    def fetch_artifact(self, src: str, dst: str) -> IO:
        """
        Method to fetch an artifact.
        """
        # Get file from remote
        key = rebuild_uri(src)
        res = api_get_call(key)
        obj = res.content

        # Store locally
        self._check_temp_dir(dst)
        name = get_name_from_uri(key)
        filepath = get_path(dst, name)
        self._store_fetched_artifact(obj, filepath)
        return filepath

    # pylint: disable=arguments-differ
    def _check_access_to_storage(self, dst: str) -> None:
        """
        Check if there is access to the storage.
        """
        try:
            check_url_availability(dst)
        except Exception as ex:
            raise ex

    def get_run_artifacts_uri(self, run_id: str) -> str:
        """
        Return the path of the artifact store for the Run.
        """
        return rebuild_uri(self.artifact_uri, run_id)

    def _parse_auth(self) -> Union[tuple]:
        if self.config is not None:
            if self.config["auth"] == "basic":
                auth = self.config["user"], self.config["password"]
            return auth
        return None
