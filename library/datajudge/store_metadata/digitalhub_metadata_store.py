"""
Implementation of REST metadata store designed by Digital Society Lab.
"""
from collections import namedtuple
from json.decoder import JSONDecodeError
from typing import Optional

from requests.models import Response  # pylint: disable=import-error

from datajudge.store_metadata.metadata_store import MetadataStore
from datajudge.utils import config as cfg
from datajudge.utils.rest_utils import api_post_call, api_put_call
from datajudge.utils.uri_utils import check_url, rebuild_uri


KeyPairs = namedtuple("KeyPairs", ("run_id", "key"))


class DigitalHubMetadataStore(MetadataStore):
    """
    Rest metadata store object.

    Allows the client to interact with the DigitalHub API backend.

    """

    def __init__(self,
                 uri_metadata: str,
                 config:  Optional[dict] = None) -> None:
        super().__init__(uri_metadata, config)
        # To memorize runs present in the backend
        self._key_vault = {
            self._RUN_METADATA: [],
            self._DATA_RESOURCE: [],
            self._SHORT_REPORT: [],
            self._SHORT_SCHEMA: [],
            self._DATA_PROFILE: [],
            self._ARTIFACT_METADATA: [],
            self._RUN_ENV: []
        }
        # API endpoints
        self._endpoints = {
            self._RUN_METADATA: cfg.API_RUN_METADATA,
            self._DATA_RESOURCE: cfg.API_DATA_RESOURCE,
            self._SHORT_REPORT: cfg.API_SHORT_REPORT,
            self._SHORT_SCHEMA: cfg.API_SHORT_SCHEMA,
            self._DATA_PROFILE: cfg.API_DATA_PROFILE,
            self._ARTIFACT_METADATA: cfg.API_ARTIFACT_METADATA,
            self._RUN_ENV: cfg.API_RUN_ENV
        }

    def init_run(self,
                 run_id: str,
                 overwrite: bool) -> None:
        """
        Check if run id is stored in the keys vault.
        Decide then if overwrite or not all runs metadata.
        """
        exist = False
        for run in self._key_vault[self._RUN_METADATA]:
            if run.run_id == run_id:
                exist = True
                break

        if overwrite:
            for i in self._key_vault:
                # Cleanup on overwrite
                self._key_vault[i] = [
                    elm for elm in self._key_vault[i] if elm.run_id != run_id]
            return
        if not overwrite and exist:
            raise RuntimeError("Id already present, please change " +
                               "it or enable overwrite.")

    def log_metadata(self,
                     metadata: dict,
                     dst: str,
                     src_type: str,
                     overwrite: bool) -> None:
        """
        Method that log metadata.
        """
        # control post/put
        key = None
        if src_type != self._ARTIFACT_METADATA:
            for elm in self._key_vault[src_type]:
                if elm.run_id == metadata["runId"]:
                    key = elm.key
        dst = self._build_source_destination(dst, src_type, key)
        kwargs = {
            "json": metadata
        }
        kwargs = self._parse_auth(kwargs)

        if key is None:
            if src_type == self._RUN_METADATA:
                kwargs["params"] = {
                    "overwrite": "true" if overwrite else "false"
                }
            response = api_post_call(dst, **kwargs)
            self._parse_response(response, src_type)
        else:
            response = api_put_call(dst, **kwargs)
            self._parse_response(response, src_type)

    def _build_source_destination(self,
                                  dst: str,
                                  src_type: str,
                                  key: Optional[str] = None
                                  ) -> str:
        """
        Return source destination API based on input source type.
        """
        key = "/" if key is None else "/" + key
        return check_url(dst + self._endpoints[src_type] + key)

    def _parse_response(self,
                        response: Response,
                        src_type: str) -> None:
        """
        Parse the JSON response from the backend APIs.
        """
        if not response.ok:
            raise Exception(response.text)

        # Jsonify
        try:
            resp = response.json()
        except JSONDecodeError as j_err:
            raise j_err

        # Get ids (run id + id stored in backend)
        run_id = resp.get("runId")
        id_ = resp.get("id")

        # Check and store key pairs in key_vault
        if run_id is not None and id_ is not None:
            new_pair = KeyPairs(run_id, id_)
            if new_pair not in self._key_vault[src_type]:
                self._key_vault[src_type].append(new_pair)
            return

        # Exception
        raise Exception("Something wrong with JSON response!")

    def get_run_metadata_uri(self,
                             run_id: Optional[str] = None) -> str:
        """
        Return the URL of the metadata store for the Run.
        """
        return self.uri_metadata

    def get_data_resource_uri(self,
                              run_id: Optional[str] = None) -> str:
        """
        Return the URL of the data resource for the Run.
        """
        url = self.uri_metadata + self._endpoints[self._DATA_RESOURCE]
        return rebuild_uri(url)

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
