from __future__ import annotations

import typing
from mimetypes import guess_type
from typing import Any, Optional

import frictionless
from datajudge.data import ShortReport
from datajudge.run import Run
from datajudge.utils.constants import FileNames, MetadataType
from frictionless import Resource
from frictionless.report import Report
from frictionless.schema import Schema

if typing.TYPE_CHECKING:
    from datajudge.client import Client
    from datajudge.data import DataResource
    from datajudge.run import RunInfo


class FrictionlessRun(Run):
    """Run object."""

    def __init__(self,
                 run_info: RunInfo,
                 data_resource: DataResource,
                 client: Client) -> None:
        super().__init__(run_info, data_resource, client)
        self._setup_run()

    def _setup_run(self) -> None:
        self._update_library_info()
        self._update_data_resource()
        self.log_data_resource()
        self._log_run()

    def _update_library_info(self) -> None:
        """Update validation library metadata."""
        self.run_info.validation_library = "frictionless"
        self.run_info.library_version = frictionless.__version__

    def _update_data_resource(self) -> None:
        frict_resource = self.get_resource()
        frict_resource.infer()
        try:
            self.data_resource.profile = frict_resource["profile"]
            self.data_resource.format = frict_resource["format"]
            if isinstance(self.data_resource.path, str):
                mediatype, _ = guess_type(self.data_resource.path)
            else:
                # Apparently frictionless fetch the first file and
                # generalize the inference to all the other files
                # e.g. if the first file is a csv and the second a
                # tsv, for the data resource all of them are csv.
                mediatype, _ = guess_type(self.data_resource.path[0])
            mediatype = mediatype if mediatype is not None else ""
            self.data_resource.mediatype = mediatype
            self.data_resource.encoding = frict_resource["encoding"]
            self.data_resource.bytes = frict_resource["stats"]["bytes"]
            self.data_resource.hash = frict_resource["stats"]["hash"]
        except KeyError as kex:
            raise kex

    def _log_run(self) -> None:
        """Log run metadata."""
        self._log_metadata(self.run_info.to_dict(),
                           MetadataType.RUN_METADATA.value)

    def log_data_resource(self) -> None:
        """Log data resource metadata."""
        self._log_metadata(self.data_resource.to_dict(),
                           MetadataType.DATA_RESOURCE.value)

    def _parse_report(self, report: Report) -> ShortReport:
        """Parse the full report to get a shorter version."""

        short_report = ShortReport(self.run_info.data_resource_uri,
                                   self.run_info.experiment_name,
                                   self.run_info.run_id)
        
        if len(report.tables) > 0:
            short_report.time = report.tables[0]["time"]
            short_report.valid = report.tables[0]["valid"]
            short_report.errors = report.tables[0]["errors"]

        return short_report

    def log_short_report(self, report: Report) -> None:
        """Log shortened report from datajudge report."""

        if not isinstance(report, Report):
            raise TypeError("Only frictionless report accepted.")

        report_short = self._parse_report(report)
        self._log_metadata(report_short.to_dict(),
                           MetadataType.SHORT_REPORT.value)

    def _log_metadata(self,
                      metadata: dict,
                      src_type: str) -> None:
        """Call client persist_metadata
        method to store a json file."""
        
        content = {
            "run_id": self.run_info.run_id,
            "experiment_id": self.run_info.experiment_id,
            "content": metadata}
        
        self.client._persist_metadata(
                            content,
                            self.run_info.run_metadata_uri,
                            src_type)

    def persist_artifact(self,
                         src: Any,
                         src_name: Optional[str] = None) -> None:
        """Call client persist_artifact
        method to store an artifact."""
        self.client._persist_artifact(
                            src,
                            self.run_info.run_artifacts_uri,
                            src_name=src_name)

    def persist_data(self) -> None:
        """Shortcut to persist the input resources
        into the artifacts storage."""
        self.persist_artifact(self.data_resource.path)
        if self.data_resource.schema is not None:
            self.persist_artifact(self.data_resource.schema)

    def persist_full_report(self, report: Report) -> None:
        """Persist full report produced by validation."""
        self.persist_artifact(
                    dict(report),
                    src_name=FileNames.FULL_REPORT.value)

    def persist_inferred_schema(self, schema: Schema) -> None:
        """Shortcut to persist inferred schema
        for a DataResource as artifact."""
        self.persist_artifact(
                    dict(schema),
                    src_name=FileNames.SCHEMA_INFERRED.value)

    def get_resource(self, **kwargs) -> Resource:
        """Return a frictionless Resource to perform
        frictionless tasks."""
        if "path" in kwargs.keys():
            kwargs.pop("path")
        return Resource(path=self.data_resource.path,
                        **kwargs)

    def validate_resource(self) -> Report:
        return frictionless.validate_resource(
                        self.get_resource(
                            schema=Schema(self.data_resource.schema)))
