from collections import namedtuple
from json.decoder import JSONDecodeError
from typing import Optional, Union

from requests.models import Response  # pylint: disable=import-error

from datajudge.store_metadata.metadata_store import MetadataStore
from datajudge.utils import config as cfg
from datajudge.utils.rest_utils import (api_post_call, api_put_call,
                                        parse_status_code, parse_url)

KeyPairs = namedtuple("KeyPairs", ("run_id", "key"))


class RestMetadataStore(MetadataStore):
    """
    Rest metadata store object.

    Allows the client to interact with the DigitalHub API backend.

    Attributes
    ----------
    _key_vault : dict
        Mapper to retain object reference presents in the backend.
    _endpoints : dict
        Mapper to backend metadata endpoints.

    Methods
    -------
    _parse_response :
        Parse the JSON response from the backend APIs.

    See also
    --------
    MetadataStore : Abstract metadata store class.

    """

    def __init__(self,
                 uri_metadata: str,
                 config:  Optional[dict] = None) -> None:
        super().__init__(uri_metadata, config)
        self._key_vault = {
            self._RUN_METADATA: [],
            self._DATA_RESOURCE: [],
            self._SHORT_REPORT: [],
            self._SHORT_SCHEMA: [],
            self._DATA_PROFILE: [],
            self._ARTIFACT_METADATA: []
        }
        self._endpoints = {
            self._RUN_METADATA: cfg.API_RUN_METADATA,
            self._DATA_RESOURCE: cfg.API_DATA_RESOURCE,
            self._SHORT_REPORT: cfg.API_SHORT_REPORT,
            self._SHORT_SCHEMA: cfg.API_SHORT_SCHEMA,
            self._DATA_PROFILE: cfg.API_DATA_PROFILE,
            self._ARTIFACT_METADATA: cfg.API_ARTIFACT_METADATA
        }

    def init_run(self,
                 run_id: str,
                 overwrite: bool) -> None:
        """
        Check if run id is cached in the store keys vault.
        Decide then if overwrite or not run metadata.

        Parameters
        ----------
        run_id : str
            A run id.
        overwrite : bool
            If True, overwrite run related metadata.

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
                if elm.run_id == metadata["run_id"]:
                    key = elm.key

        dst = self._build_source_destination(dst, src_type, key)
        auth = self.parse_auth()

        if key is None:
            if src_type == self._RUN_METADATA:
                params = {"overwrite": "true" if overwrite else "false"}
                response = api_post_call(metadata,
                                         dst,
                                         auth=auth,
                                         params=params)
            else:
                response = api_post_call(metadata, dst, auth=auth)
            self._parse_response(response, src_type)
        else:
            response = api_put_call(metadata, dst, auth=auth)

    def _build_source_destination(self,
                                  dst: str,
                                  src_type: str,
                                  key: Optional[str] = None
                                  ) -> str:
        """
        Return source destination API based on input source type.
        """
        key = "/" + key if key is not None else "/"
        return parse_url(dst + self._endpoints[src_type] + key)

    def _parse_response(self,
                        response: Response,
                        src_type: str) -> None:
        """
        Parse the JSON response from the backend APIs.
        """
        parse_status_code(response)
        try:
            resp = response.json()
            keys = resp.keys()
            if "run_id" in keys and "id" in keys:
                new_pair = KeyPairs(resp["run_id"], resp["id"])
                if new_pair not in self._key_vault[src_type]:
                    self._key_vault[src_type].append(new_pair)
        except JSONDecodeError as j_err:
            raise j_err
        except Exception as ex:
            raise ex

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
        endpoint = self._endpoints[self._DATA_RESOURCE]
        return parse_url(self.uri_metadata + endpoint)

    def parse_auth(self) -> Union[tuple]:
        if self.config:
            if self.config["auth"] == "basic":
                auth = self.config["user"], self.config["password"]
            return auth
        return None
