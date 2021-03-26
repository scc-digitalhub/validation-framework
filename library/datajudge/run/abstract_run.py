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
    _RUN_METADATA = MetadataType.RUN_METADATA.value
    _DATA_RESOURCE = MetadataType.DATA_RESOURCE.value
    _SHORT_REPORT = MetadataType.SHORT_REPORT.value
    _ARTIFACT_METADATA = MetadataType.ARTIFACT_METADATA.value

    def __init__(self,
                 run_info: RunInfo,
                 data_resource: DataResource,
                 client: Client,
                 overwrite: bool) -> None:

        self._data_resource = data_resource
        self._client = client
        self._run_info = run_info
        self._overwrite = overwrite

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
        return ShortReport(self._run_info.data_resource_uri,
                           self._run_info.experiment_name,
                           self._run_info.run_id)

    def _get_content(self, cont: Optional[dict] = None) -> dict:
        """
        Return structured content to log.
        """
        content = {
            "run_id": self._run_info.run_id,
            "experiment_id": self._run_info.experiment_id,
            "experiment_name": self._run_info.experiment_name,
            "contents": cont
        }
        return content

    def get_run(self) -> dict:
        """
        Return a dictionary of run info attributes.
        """
        return self._run_info.to_dict()

    def __enter__(self) -> Run:
        # Set run status
        self._run_info.begin_status = "active"
        self._run_info.started = get_time()

        # Log data resource
        self.log_data_resource()

        # Update run info
        uri_res = self._client._get_data_resource_uri(
                                        self._run_info.run_id)
        self._run_info.data_resource_uri = uri_res
        self._log_run()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if exc_type in (InterruptedError, KeyboardInterrupt):
            self._run_info.end_status = "interrupted"
        elif exc_type in (OSError, NotImplementedError):
            self._run_info.end_status = "failed"
        else:
            self._run_info.end_status = "finished"
        self._run_info.finished = get_time()
        self._log_run()

    def __repr__(self) -> str:
        return str(self._run_info.to_dict())
