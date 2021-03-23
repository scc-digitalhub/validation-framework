from typing import Optional

from requests.models import Response

from datajudge.store_metadata.metadata_store import MetadataStore
from datajudge.utils.constants import MetadataType, ApiEndpoint
from datajudge.utils.rest_utils import (api_delete_call, api_get_call,
                                        api_post_call, api_put_call, parse_url)


class RestMetadataStore(MetadataStore):
    """
    Rest store to interact with the DigitalHub API service.

    Attributes
    ----------
    _key_vault :
        Mapper to retain object reference presents in the MongoDB.

    Methods
    -------
    parse_response :
        Parse the JSON response from the backend APIs.

    """

    def __init__(self,
                 uri_metadata: str,
                 credentials:  Optional[dict] = None) -> None:
        super().__init__(uri_metadata, credentials)
        self._key_vault = {
            MetadataType.RUN_METADATA.value: [],
            MetadataType.SHORT_REPORT.value: [],
            MetadataType.DATA_RESOURCE.value: []
        }

    def check_run(self,
                  run_id: str,
                  overwrite: bool) -> None:
        """
        Check run id existence.
        """
        pass

    def persist_metadata(self,
                         contents: dict,
                         dst: str,
                         src_type: str) -> None:
        """
        Method that persist metadata.
        """
        # control post/put
        key = None
        for elm in self._key_vault[src_type]:
            if isinstance(elm, dict):
                if elm["run_id"] == contents["run_id"]:
                    key = elm["key"]

        dst = self._build_source_destination(dst, src_type, key)

        if key is None:
            response = api_post_call(contents, dst)
            self.parse_response(response, src_type)
        else:
            api_put_call(contents, dst)

    @staticmethod
    def _build_source_destination(dst:str,
                                  src_type: str,
                                  key: Optional[str] = None) -> str:
        """
        Return source destination API based on input source type.
        """

        key = key if key is not None else ""

        if src_type == MetadataType.RUN_METADATA.value:
            endpoint = ApiEndpoint.RUN.value
        elif src_type == MetadataType.SHORT_REPORT.value:
            endpoint = ApiEndpoint.SHORT_REPORT.value
        elif src_type == MetadataType.DATA_RESOURCE.value:
            endpoint = ApiEndpoint.DATA_RESOURCE.value
        else:
            raise RuntimeError("No such metadata type.")
        return parse_url(dst + endpoint + key)

    def parse_response(self,
                       response: Response,
                       src_type: str) -> None:
        """
        Parse the JSON response from the backend APIs.
        """
        try:
            contents = response.json()
            self._key_vault[src_type].append(contents)
        except:
            raise

    def get_run_metadata_uri(self,
                             run_id: Optional[str] = None) -> str:
        """
        Return the URL of the metadata store for the Run.
        """
        return self.uri_metadata

    def get_data_resource_uri(self, run_id: str) -> str:
        """
        Return the URL of the data resource for the Run.
        """
        return parse_url(self.uri_metadata + ApiEndpoint.DATA_RESOURCE.value)
