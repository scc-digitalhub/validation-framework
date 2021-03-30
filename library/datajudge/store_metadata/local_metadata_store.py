from typing import Optional

from datajudge.store_metadata.metadata_store import MetadataStore
from datajudge.utils.constants import FileNames
from datajudge.utils.file_utils import (check_dir, get_path, make_dir,
                                        remove_files, write_json)


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
                 config:  Optional[dict] = None) -> None:
        super().__init__(uri_metadata, config)
        self.filenames = {
            self.RUN_METADATA: FileNames.RUN_METADATA.value,
            self.SHORT_REPORT: FileNames.SHORT_REPORT.value,
            self.DATA_RESOURCE: FileNames.DATA_RESOURCE.value,
            self.ARTIFACT_METADATA: FileNames.ARTIFACT_METADATA.value
        }
        self.artifact_count = 0

    def init_run(self,
                 run_id: str,
                 overwrite: bool) -> None:
        """
        Check run enviroment existence. If folder
        doesn't exist, create or recreate it.
        """
        uri = self.get_run_metadata_uri(run_id)
        self._check_dst_folder(uri, overwrite, init=True)

    def log_metadata(self,
                     metadata: dict,
                     dst: str,
                     src_type: str,
                     overwrite: bool) -> None:
        """
        Method that log metadata.
        """
        self._check_dst_folder(dst, overwrite)
        dst = self._build_source_destination(dst, src_type)
        write_json(metadata, dst)

    def _check_dst_folder(self,
                          dst: str,
                          overwrite: bool,
                          init: Optional[bool] = False) -> None:
        """
        Check if run folder already exist, otherwise it creates it.
        """
        if check_dir(dst):
            if not overwrite:
                raise OSError("Run already exists, please use another id")
            if init and overwrite:
                self.artifact_count = 0
                remove_files(dst)
        else:
            make_dir(dst)

    def _build_source_destination(self,
                                  dst: str,
                                  src_type: str,
                                  key: Optional[str] = None) -> str:
        """
        Return source path based on input source type.
        """
        filename = self.filenames[src_type]
        if src_type == self.ARTIFACT_METADATA:
            filename = filename.format(self.artifact_count)
            self.artifact_count += 1
        return get_path(dst, filename)

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
