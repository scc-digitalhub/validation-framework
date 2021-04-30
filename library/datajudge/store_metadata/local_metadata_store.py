"""
Implementation of local metadata store.
"""
from typing import Optional

from datajudge.store_metadata.metadata_store import MetadataStore
from datajudge.utils import config as cfg
from datajudge.utils.file_utils import (check_dir, get_path, make_dir,
                                        remove_files, write_json)


class LocalMetadataStore(MetadataStore):
    """
    Local metadata store object.

    Allows the client to interact with local filesystem.

    Attributes
    ----------
    _filenames : dict
        Mapper for output filenames.
    _artifact_count : int
        Counter to number artifact stored metadata.

    Methods
    -------
    _check_dst_folder :
        Check if run folder already exist, otherwise it creates it.

    See also
    --------
    MetadataStore : Abstract metadata store class.

    """

    def __init__(self,
                 uri_metadata: str,
                 config:  Optional[dict] = None) -> None:
        super().__init__(uri_metadata, config)
        self._filenames = {
            self._RUN_METADATA: cfg.FN_RUN_METADATA,
            self._DATA_RESOURCE: cfg.FN_DATA_RESOURCE,
            self._SHORT_REPORT: cfg.FN_SHORT_REPORT,
            self._SHORT_SCHEMA: cfg.FN_SHORT_SCHEMA,
            self._DATA_PROFILE: cfg.FN_DATA_PROFILE,
            self._ARTIFACT_METADATA: cfg.FN_ARTIFACT_METADATA
        }
        self._artifact_count = 0

    def init_run(self,
                 run_id: str,
                 overwrite: bool) -> None:
        """
        Check run metadata folder existence.
        If folder doesn't exist, create it.
        If overwrite is True, it delete all the run's folder contents.
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
                self._artifact_count = 0
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
        filename = self._filenames[src_type]
        if src_type == self._ARTIFACT_METADATA:
            filename = filename.format(self._artifact_count)
            self._artifact_count += 1
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
        filename = self._filenames[self._DATA_RESOURCE]
        return get_path(self.uri_metadata,
                        run_id,
                        filename)
