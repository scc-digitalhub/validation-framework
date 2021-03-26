from typing import Optional

from datajudge.store_metadata.metadata_store import MetadataStore
from datajudge.utils.constants import FileNames
from datajudge.utils.file_utils import (check_dir, get_path, make_dir,
                                        write_json)


class LocalMetadataStore(MetadataStore):
    """
    Rest store to interact with local filesystem.

    Attributes
    ----------
    _key_vault :
        Mapper to retain object reference presents in the MongoDB.

    Methods
    -------
    _check_dst_folder :
        Check if run folder already exist, otherwise it creates it.

    """

    def __init__(self,
                 uri_metadata: str,
                 credentials:  Optional[dict] = None) -> None:
        super().__init__(uri_metadata, credentials)
        self.filenames = {
            self.RUN_METADATA: FileNames.RUN_METADATA.value,
            self.SHORT_REPORT: FileNames.SHORT_REPORT.value,
            self.DATA_RESOURCE: FileNames.DATA_RESOURCE.value,
            self.ARTIFACT_METADATA: FileNames.ARTIFACT_METADATA.value
        }

    def persist_metadata(self,
                         metadata: dict,
                         dst: str,
                         src_type: str,
                         overwrite: bool) -> None:
        """
        Method that persist metadata.
        """
        self._check_dst_folder(dst, overwrite)
        dst = self._build_source_destination(dst, src_type)
        write_json(metadata, dst)

    @staticmethod
    def _check_dst_folder(dst: str,
                          overwrite: bool) -> None:
        """
        Check if run folder already exist, otherwise it creates it.
        """
        if check_dir(dst):
            if not overwrite:
                raise OSError("Run already exists, please use another id")
        else:
            make_dir(dst)

    def _build_source_destination(self,
                                  dst: str,
                                  src_type: str,
                                  key: Optional[str] = None) -> str:
        """
        Return source path based on input source type.
        """
        return get_path(dst, self.filenames[src_type])

    def get_run_metadata_uri(self, run_id: str) -> str:
        """
        Return the path of the metadata folder for the Run.
        """
        return get_path(self.uri_metadata, run_id)

    def get_data_resource_uri(self, run_id: str) -> str:
        """
        Return the path of the data resource for the Run.
        """
        return get_path(self.uri_metadata,
                        run_id,
                        FileNames.DATA_RESOURCE.value)
