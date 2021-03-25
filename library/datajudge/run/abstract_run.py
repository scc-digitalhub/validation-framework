from __future__ import annotations

import typing
from abc import ABCMeta, abstractmethod
from typing import Any, Optional

from datajudge.utils.constants import MetadataType
from datajudge.data import ShortReport
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

    run_info :
        The metadata set of the run.
    data_resource :
        A DataResource object.
    client:
        A Client object that interact with the storages.
    overwrite :
        Boolean describing whether a run with same id should be
        overwritten

    Methods
    -------
    _log_run :
        Method to log run's metadata.
    log_data_resource :
        Method to log data resource.
    _log_metadata :
        Method to log generic metadata.
        It interacts directly with the client.
    persist_artifact :
        Method to persist artifacts in the artifact store.
    persist_data :
        Shortcut to persist data and validation schema.
    _update_library_info :
        Update run's info about the validation framework used.
    _update_data_resource :
        Update resource with inferred information.
    _parse_report :
        Parse the report produced by the validation framework.
    log_short_report :
        Method to log short report.
    persist_full_report :
        Shortcut to persist the full report produced by the validation
        framework as artifact.
    persist_inferred_schema :
        Shortcut to persist the inferred schema produced by the
        validation framework as artifact.
    get_resource :
        Return a resource object specific of the library.
    get_short_report :
        Return a ShortReport object.
    _get_content :
        Return structured content to log.

    """

    __metaclass__ = ABCMeta
    RUN_METADATA = MetadataType.RUN_METADATA.value
    DATA_RESOURCE = MetadataType.DATA_RESOURCE.value
    SHORT_REPORT = MetadataType.SHORT_REPORT.value
    ARTIFACT_METADATA = MetadataType.ARTIFACT_METADATA.value

    def __init__(self,
                 run_info: RunInfo,
                 data_resource: DataResource,
                 client: Client,
                 overwrite: bool) -> None:

        self.data_resource = data_resource
        self.client = client
        self.run_info = run_info
        self.overwrite = overwrite

    @abstractmethod
    def _log_run(self) -> None:
        """
        Method to log run's metadata.
        """
        pass

    @abstractmethod
    def log_data_resource(self) -> None:
        """
        Method to log data resource.
        """
        pass

    @abstractmethod
    def _log_metadata(self,
                      metadata: dict,
                      src_type: Optional[str] = None) -> None:
        """
        Method to log generic metadata.
        """
        pass

    @abstractmethod
    def persist_artifact(self,
                         src: Any,
                         src_name: Optional[str] = None) -> None:
        """
        Method to persist artifacts in the artifact store.
        """
        pass

    @abstractmethod
    def persist_data(self) -> None:
        """
        Shortcut to persist data and validation schema.
        """
        pass

    @abstractmethod
    def _update_library_info(self) -> None:
        """
        Update run's info about the validation framework used.
        """
        pass

    @abstractmethod
    def _update_data_resource(self) -> None:
        """
        Update resource with inferred information.
        """
        pass

    @abstractmethod
    def _parse_report(self, report: Any) -> ShortReport:
        """
        Parse the report produced by the validation framework.
        """
        pass

    @abstractmethod
    def log_short_report(self, report: Any) -> None:
        """
        Method to log short report.
        """
        pass

    @abstractmethod
    def persist_full_report(self, report: Any) -> None:
        """
        Shortcut to persist the full report produced by the
        validation framework as artifact.
        """
        pass

    @abstractmethod
    def persist_inferred_schema(self, schema: Any) -> None:
        """
        Shortcut to persist the inferred schema produced by the
        validation framework as artifact.
        """
        pass

    @abstractmethod
    def get_resource(self) -> Any:
        """
        Return a resource object specific of the library.
        """
        pass

    def _get_short_report(self) -> ShortReport:
        """
        Return a ShortReport object.
        """
        return ShortReport(self.run_info.data_resource_uri,
                           self.run_info.experiment_name,
                           self.run_info.run_id)

    def _get_content(self, cnt: Optional[dict] = None) -> dict:
        """
        Return structured content to log.
        """
        content = {
            "run_id": self.run_info.run_id,
            "experiment_id": self.run_info.experiment_id,
            "experiment_name": self.run_info.experiment_name,
            "content": cnt
        }
        return content

    def __enter__(self) -> Run:
        self.run_info.begin_status = "active"
        self.run_info.started = get_time()
        self.log_data_resource()
        self._log_run()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type in (InterruptedError, KeyboardInterrupt):
            self.run_info.end_status = "interrupted"
        elif exc_type in (OSError, NotImplementedError):
            self.run_info.end_status = "failed"
        else:
            self.run_info.end_status = "finished"
        self.run_info.finished = get_time()
        self._log_run()

    def __repr__(self) -> str:
        return str(self.run_info.__dict__)
