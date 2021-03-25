from typing import Optional

from requests.models import Response  # pylint: disable=import-error
from datajudge.store_metadata.metadata_store import MetadataStore
from datajudge.utils.constants import ApiEndpoint, MetadataType
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
            MetadataType.DATA_RESOURCE.value: [],
            MetadataType.ARTIFACT.value: []
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
            if isinstance(elm, dict):
                if elm["run_id"] == metadata["run_id"]:
                    key = elm["id"]

        dst = self._build_source_destination(dst, src_type, key)

        if key is None:
            if src_type == MetadataType.RUN_METADATA.value:
                params = {"overwrite": overwrite}
                response = api_post_call(metadata, dst, params)
            else:
                response = api_post_call(metadata, dst)
            self.parse_response(response, src_type)
        else:
            api_put_call(metadata, dst)

    @staticmethod
    def _build_source_destination(dst: str,
                                  src_type: str,
                                  key: Optional[str] = None
                                  ) -> str:
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
        elif src_type == MetadataType.ARTIFACT.value:
            endpoint = ApiEndpoint.ARTIFACT.value
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
            resp = response.json()
            self._key_vault[src_type].append(resp)
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
        return parse_url(self.uri_metadata + ApiEndpoint.DATA_RESOURCE.value)
