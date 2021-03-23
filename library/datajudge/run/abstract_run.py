from __future__ import annotations

import typing
from abc import ABCMeta, abstractmethod
from typing import Any, Optional

from datajudge.utils.time_utils import get_time

if typing.TYPE_CHECKING:
    from datajudge.client import Client
    from datajudge.data import DataResource, ShortReport
    from datajudge.run import RunInfo


class Run:
    """Run object."""

    __metaclass__ = ABCMeta
    
    def __init__(self,
                 run_info: RunInfo,
                 data_resource: DataResource,
                 client: Client) -> None:

        self.data_resource = data_resource
        self.client = client
        self.run_info = run_info

    @abstractmethod
    def _log_run(self) -> None:
        """Log run metadata."""
        pass

    @abstractmethod
    def log_data_resource(self) -> None:
        """Log data resource metadata."""
        pass

    @abstractmethod
    def _log_metadata(self,
                      metadata: dict,
                      src_type: Optional[str] = None) -> None:
        """Call client persist_metadata
        method to store a metadata json."""
        pass

    @abstractmethod
    def persist_artifact(self,
                         src: Any,
                         src_name: Optional[str] = None) -> None:
        """Call client persist_artifact
        method to store an artifact."""
        pass

    @abstractmethod
    def persist_data(self) -> None:
        """Shortcut to persist the input resources
        into the artifacts storage."""
        pass

    @abstractmethod
    def _setup_run(self) -> None:
        """Preliminary run operations
        (log data_resource, log_run)."""
        pass

    @abstractmethod
    def _update_library_info(self) -> None:
        """Update validation library metadata."""
        pass

    @abstractmethod
    def _parse_report(self, report: Any) -> ShortReport:
        """Parse the full report to get a shorter version."""
        pass
    
    @abstractmethod
    def log_short_report(self, report: Any) -> None:
        """Log shortened report from datajudge report."""
        pass

    @abstractmethod
    def persist_full_report(self, report: Any) -> None:
        """Persist full report produced by validation."""
        pass

    @abstractmethod
    def persist_inferred_schema(self, schema: Any) -> None:
        """Shortcut to persist inferred schema
        for a DataResource as artifact."""
        pass

    @abstractmethod
    def get_resource(self) -> Any:
        """Return a Resource based on the validation library."""
        pass

    def __enter__(self) -> Run:
        self.run_info.begin_status = "active"
        self.run_info.started = get_time()
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
