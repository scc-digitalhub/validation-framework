from typing import Optional

from requests.models import Response

from datajudge.store_metadata.metadata_store import MetadataStore
from datajudge.utils.constants import MetadataType, ApiEndpoint
from datajudge.utils.rest_utils import (api_delete_call, api_get_call,
                                        api_post_call, api_put_call, parse_url)


class RestMetadataStore(MetadataStore):
    """Rest store."""

    def __init__(self,
                 uri_metadata: str,
                 credentials:  Optional[dict] = None) -> None:
        super().__init__(uri_metadata, credentials)
        self._key_vault = {
            MetadataType.RUN_METADATA.value: [],
            MetadataType.SHORT_REPORT.value: [],
            MetadataType.DATA_RESOURCE.value: []
        }

    def create_run_enviroment(self,
                              run_id: str,
                              overwrite: bool) -> None:
        """Create the run enviroment."""
        pass

    def persist_metadata(self,
                         contents: dict,
                         dst: str,
                         src_type: str) -> None:

        # control post/put
        key = None
        for elm in self._key_vault[src_type]:
            if isinstance(elm, dict):
                if elm["run_id"] == contents["run_id"]:
                    key = elm["key"]

        dst = self.build_source_destination(dst, src_type, key)

        if key is None:
            response = api_post_call(contents, dst)
            self.parse_response(response, src_type)
        else:
            api_put_call(contents, dst)

    @staticmethod
    def _build_source_destination(dst:str,
                                 src_type: str,
                                 key: Optional[str] = None) -> str:
        """Return source destination based
        on source type."""

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
        try:
            contents = response.json()
            self._key_vault[src_type].append(contents)
        except:
            raise

    def get_run_metadata_uri(self,
                             run_id: Optional[str] = None) -> str:
        """Return the URI for the run metadata"""
        return self.uri_metadata

    def get_data_resource_uri(self, run_id: str) -> str:
        """Return the URI of the data_resource"""
        return parse_url(self.uri_metadata + ApiEndpoint.DATA_RESOURCE.value)
