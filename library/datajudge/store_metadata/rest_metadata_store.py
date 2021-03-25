from json.decoder import JSONDecodeError
from typing import Optional

from requests.models import Response  # pylint: disable=import-error
from datajudge.store_metadata.metadata_store import MetadataStore
from datajudge.utils.constants import ApiEndpoint
from datajudge.utils.rest_utils import api_post_call, api_put_call, parse_url


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
                 credentials:  Optional[dict] = None) -> None:
        super().__init__(uri_metadata, credentials)
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

    def persist_metadata(self,
                         metadata: dict,
                         dst: str,
                         src_type: str,
                         overwrite: bool) -> None:
        """
        Method that persist metadata.
        """
        # control post/put
        key = None
        for elm in self._key_vault[src_type]:
            if elm["run_id"] == metadata["run_id"] and overwrite:
                key = elm["key"]

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
        try:
            resp = response.json()
            if "run_id" in resp.keys() and "id" in resp.keys():
                new_key = {"run_id": resp["run_id"],
                           "key": resp["id"]}
                self._key_vault[src_type].append(new_key)
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
