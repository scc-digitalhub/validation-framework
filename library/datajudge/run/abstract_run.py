"""
AbstractRun module.
Implementations of a Run abstract class.
"""
from __future__ import annotations

import typing
from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List, Optional

from datajudge.utils.constants import FileNames, MetadataType
from datajudge.data import ShortReport, ShortSchema
from datajudge.utils.time_utils import get_time

if typing.TYPE_CHECKING:
    from datajudge.client import Client
    from datajudge.data import DataResource
    from datajudge.run import RunInfo


class Run:
    """
    Run abstract object.
    The run is the main interface to interact with data and metadata.
    It interacts both with the Client and the Data Resource/Package.

    Attributes
    ----------
    run_info : RunInfo
        The metadata info of the run.
    data_resource : DataResource
        A DataResource object.
    client : Client
        A Client object that interact with the storages.

    Methods
    -------
    get_run :
        Return Run Info as dictionary.

    """

    __metaclass__ = ABCMeta
    _RUN_METADATA = MetadataType.RUN_METADATA.value
    _DATA_RESOURCE = MetadataType.DATA_RESOURCE.value
    _SHORT_REPORT = MetadataType.SHORT_REPORT.value
    _SHORT_SCHEMA = MetadataType.SHORT_SCHEMA.value
    _DATA_PROFILE = MetadataType.DATA_PROFILE.value
    _ARTIFACT_METADATA = MetadataType.ARTIFACT_METADATA.value
    _FULL_REPORT = FileNames.FULL_REPORT.value
    _SCHEMA_INFERRED = FileNames.SCHEMA_INFERRED.value
    _FULL_PROFILE = FileNames.FULL_PROFILE.value

    def __init__(self,
                 run_info: RunInfo,
                 data_resource: DataResource,
                 client: Client,
                 overwrite: bool) -> None:

        self.data_resource = data_resource
        self.client = client
        self.run_info = run_info
        self._overwrite = overwrite

    @abstractmethod
    def _update_library_info(self) -> None:
        """
        Update run's info about the validation framework used.
        """

    @abstractmethod
    def _log_run(self) -> None:
        """
        Method to log run's metadata.
        """

    @abstractmethod
    def _update_data_resource(self) -> None:
        """
        Update resource with inferred information.
        """

    @abstractmethod
    def log_data_resource(self, infer: bool = False) -> None:
        """
        Method to log data resource.
        """

    @abstractmethod
    def _parse_report(self, report: Any) -> ShortReport:
        """
        Parse the report produced by the validation framework.
        """

    @abstractmethod
    def _check_report(self, report: Any) -> None:
        """
        Check a report before log/persist it.
        """

    @abstractmethod
    def log_short_report(self, report: Any) -> None:
        """
        Method to log short report.
        """

    @abstractmethod
    def _infer_schema(self) -> Any:
        """
        Parse the inferred schema produced by the validation
        framework.
        """

    @abstractmethod
    def _parse_schema(self, schema: Any) -> ShortSchema:
        """
        Parse the inferred schema produced by the validation
        framework.
        """

    @abstractmethod
    def _check_schema(self, schema: Any) -> None:
        """
        Check a schema before log/persist it.
        """

    @abstractmethod
    def log_short_schema(self, schema: Any) -> None:
        """
        Method to log short schema.
        """

    @abstractmethod
    def _parse_profile(self, profile: Any) -> Any:
        """
        Parse the profile generated by pandas profiling.
        """

    @abstractmethod
    def log_profile(self, profile: Any) -> None:
        """
        Method to log a pandas profile.
        """

    @abstractmethod
    def _log_artifact(self,
                      src: Any,
                      src_name: Optional[str]
                      ) -> None:
        """
        Method to log artifacts metadata.
        """

    @abstractmethod
    def _log_metadata(self,
                      metadata: dict,
                      src_type: str) -> None:
        """
        Method to log generic metadata.
        """

    @abstractmethod
    def persist_data(self,
                     data_name: Optional[str] = None,
                     schema_name: Optional[str] = None) -> None:
        """
        Shortcut to persist data and validation schema.
        """

    @abstractmethod
    def persist_full_report(self, report: Any) -> None:
        """
        Shortcut to persist the full report produced by the
        validation framework as artifact.
        """

    @abstractmethod
    def persist_inferred_schema(self, schema: Any) -> None:
        """
        Shortcut to persist the inferred schema produced by the
        validation framework as artifact.
        """

    @abstractmethod
    def persist_profile(self, profile: Any) -> None:
        """
        Shortcut to persist the profile made with pandas
        profiling.
        """

    @abstractmethod
    def persist_artifact(self,
                         src: Any,
                         src_name: Optional[str] = None) -> None:
        """
        Method to persist artifacts in the artifact store.
        """

    @abstractmethod
    def get_resource(self) -> Any:
        """
        Return a resource object specific of the library.
        """

    def _get_short_report(self) -> ShortReport:
        """
        Return a ShortReport object.
        """
        return ShortReport(self.run_info.data_resource_uri,
                           self.run_info.experiment_name,
                           self.run_info.run_id)

    @staticmethod
    def _get_short_schema(fields: List[Dict[str, str]]) -> ShortSchema:
        """
        Return a ShortSchema object.
        """
        return ShortSchema(fields)

    def _get_content(self, cont: Optional[dict] = None) -> dict:
        """
        Return structured content to log.
        """
        content = {
            "run_id": self.run_info.run_id,
            "experiment_id": self.run_info.experiment_id,
            "experiment_name": self.run_info.experiment_name,
            "contents": cont
        }
        return content

    def _get_artifact_metadata(self,
                               name: str,
                               uri: str) -> dict:
        metadata = self._get_content()
        metadata.pop("contents")
        metadata["name"] = name
        metadata["uri"] = uri
        return metadata

    def get_run(self) -> dict:
        """
        Return a dictionary of run info attributes.
        """
        return self.run_info.to_dict()

    def __enter__(self) -> Run:
        # Set run status
        self.run_info.begin_status = "active"
        self.run_info.started = get_time()
        self._log_run()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type is None:
            self.run_info.end_status = "finished"
        elif exc_type in (InterruptedError, KeyboardInterrupt):
            self.run_info.end_status = "interrupted"
        elif self.run_info.data_resource_uri is None:
            self.run_info.end_status = "invalid"
        else:
            self.run_info.end_status = "failed"
        self.run_info.finished = get_time()
        self._log_run()

    def __repr__(self) -> str:
        return str(self.run_info.to_dict())
