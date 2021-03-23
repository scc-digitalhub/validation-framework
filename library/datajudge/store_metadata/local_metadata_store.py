from typing import Optional
from datajudge.store_metadata.metadata_store import MetadataStore
from datajudge.utils.constants import FileNames, MetadataType
from datajudge.utils.file_utils import (check_dir, get_path, make_dir,
                                         write_json)


class LocalMetadataStore(MetadataStore):
    """Local store."""

    def __init__(self,
                 uri_metadata: str,
                 credentials:  Optional[dict] = None) -> None:
        super().__init__(uri_metadata, credentials)

    def create_run_enviroment(self,
                              run_id: str,
                              overwrite: bool) -> None:
        """Check if run folder already exist,
        otherwise it creates it."""
        uri = self.get_run_metadata_uri(run_id)
        if check_dir(uri):
            if overwrite:
                raise OSError("Run already exists, please use another id")
        else:
            make_dir(uri)

    def persist_metadata(self,
                         src: dict,
                         dst: str,
                         src_type: str) -> None:
        """Method to persist metadata locally."""
        dst = self._build_source_destination(dst, src_type)
        write_json(src, dst)

    @staticmethod
    def _build_source_destination(dst: str,
                                 src_type: str) -> str:
        """Return source destination based
        on source type."""

        if src_type == MetadataType.RUN_METADATA.value:
            src_name = FileNames.RUN_METADATA.value
        elif src_type == MetadataType.SHORT_REPORT.value:
            src_name = FileNames.SHORT_REPORT.value
        elif src_type == MetadataType.DATA_RESOURCE.value:
            src_name = FileNames.DATA_RESOURCE.value
        else:
            raise RuntimeError("No such metadata type.")

        return get_path(dst, src_name)

    def get_run_metadata_uri(self, run_id: str) -> str:
        """Return the URI for the run metadata"""
        return get_path(self.uri_metadata, run_id)

    def get_data_resource_uri(self, run_id: str) -> str:
        """Return the URI of the data_resource"""
        return get_path(self.uri_metadata, run_id, FileNames.DATA_RESOURCE.value)
