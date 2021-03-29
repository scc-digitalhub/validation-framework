from collections import namedtuple
from json.decoder import JSONDecodeError
from typing import Optional

from requests.models import Response  # pylint: disable=import-error
from datajudge.store_metadata.metadata_store import MetadataStore
from datajudge.utils.constants import ApiEndpoint
from datajudge.utils.rest_utils import api_post_call, api_put_call, parse_url


KeyPairs = namedtuple("KeyPairs", ("run_id", "key"))


class RestMetadataStore(MetadataStore):
    """
    Rest store to interact with the DigitalHub API service.

    Attributes
    ----------
    _key_vault :
        Mapper to retain object reference presents in the MongoDB.

    Methods
    -------
    _parse_response :
        Parse the JSON response from the backend APIs.

    """

    def __init__(self,
                 uri_metadata: str,
                 config:  Optional[dict] = None) -> None:
        super().__init__(uri_metadata, config)
        self._key_vault = {
            self.RUN_METADATA: [],
            self.SHORT_REPORT: [],
            self.DATA_RESOURCE: [],
            self.ARTIFACT_METADATA: []
        }
        self.endpoints = {
            self.RUN_METADATA: ApiEndpoint.RUN_METADATA.value,
            self.SHORT_REPORT: ApiEndpoint.SHORT_REPORT.value,
            self.DATA_RESOURCE: ApiEndpoint.DATA_RESOURCE.value,
            self.ARTIFACT_METADATA: ApiEndpoint.ARTIFACT_METADATA.value
        }

    def init_run(self,
                 run_id: str,
                 overwrite: bool) -> None:
        """
        Check if run id is cached in the store keys vault.
        Decide then if overwrite or not run metadata.
        """
        exist = False
        for run in self._key_vault[self.RUN_METADATA]:
            if run.run_id == run_id:
                exist = True
                break

        if overwrite:
            for i in self._key_vault.keys():
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
        if src_type != self.ARTIFACT_METADATA:
            for elm in self._key_vault[src_type]:
                if elm.run_id == metadata["run_id"]:
                    key = elm.key

        dst = self._build_source_destination(dst, src_type, key)

        if key is None:
            if src_type == self.RUN_METADATA:
                params = {"overwrite": "true" if overwrite else "false"}
                response = api_post_call(metadata, dst, params)
            else:
                response = api_post_call(metadata, dst)
            self._parse_response(response, src_type)
        else:
            response = api_put_call(metadata, dst)

    def _build_source_destination(self,
                                  dst: str,
                                  src_type: str,
                                  key: Optional[str] = None
                                  ) -> str:
        """
        Return source destination API based on input source type.
        """
        key = "/" + key if key is not None else "/"
        return parse_url(dst + self.endpoints[src_type] + key)

    def _parse_response(self,
                        response: Response,
                        src_type: str) -> None:
        """
        Parse the JSON response from the backend APIs.
        """
        if response.status_code == 400:
            raise RuntimeError("Id already present, please change it " +
                               "or enable overwrite.")
        try:
            resp = response.json()
            keys = resp.keys()
            if "run_id" in keys and "id" in keys:
                new_pair = KeyPairs(resp["run_id"], resp["id"])
                if new_pair not in self._key_vault[src_type]:
                    self._key_vault[src_type].append(new_pair)
        except JSONDecodeError as jx:
            raise jx
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
        return parse_url(self.uri_metadata +
                         ApiEndpoint.DATA_RESOURCE.value)
