from __future__ import annotations

import typing
from mimetypes import guess_type
from typing import Any, Optional

import frictionless
from datajudge.run import Run
from datajudge.utils.constants import FileNames
from frictionless import Resource
from frictionless.report import Report
from frictionless.schema import Schema

if typing.TYPE_CHECKING:
    from datajudge.client import Client
    from datajudge.data import DataResource
    from datajudge.data import ShortReport
    from datajudge.run import RunInfo


class FrictionlessRun(Run):
    """
    Frictionless flavoured run. Inherits from Run.
    """

    def __init__(self,
                 run_info: RunInfo,
                 data_resource: DataResource,
                 client: Client,
                 overwrite: bool) -> None:
        super().__init__(run_info,
                         data_resource,
                         client,
                         overwrite)
        self._log_run()
        self._update_library_info()
        self._update_data_resource()

    def _update_library_info(self) -> None:
        """
        Update run's info about the validation framework used.
        """
        self._run_info.validation_library = frictionless.__name__
        self._run_info.library_version = frictionless.__version__

    def _update_data_resource(self) -> None:
        """
        Update resource with inferred information.
        """
        frict_resource = self.get_resource()
        frict_resource.infer()
        try:
            self._data_resource.profile = frict_resource["profile"]
            self._data_resource.format = frict_resource["format"]
            if isinstance(self._data_resource.path, str):
                mediatype, _ = guess_type(self._data_resource.path)
            else:
                # Apparently frictionless fetch the first file and
                # generalize the inference to all the other files
                # e.g. if the first file is a csv and the second a
                # tsv, for the data resource all of them are csv.
                mediatype, _ = guess_type(self._data_resource.path[0])
            mediatype = mediatype if mediatype is not None else ""
            self._data_resource.mediatype = mediatype
            self._data_resource.encoding = frict_resource["encoding"]
            self._data_resource.bytes = frict_resource["stats"]["bytes"]
            self._data_resource.hash = frict_resource["stats"]["hash"]
        except KeyError as kex:
            raise kex

    def _log_run(self) -> None:
        """
        Method to log run's metadata.
        """
        metadata = self._get_content(self._run_info.to_dict())
        self._log_metadata(metadata, self._RUN_METADATA)

    def log_data_resource(self) -> None:
        """
        Method to log data resource.
        """
        metadata = self._get_content(self._data_resource.to_dict())
        self._log_metadata(metadata, self._DATA_RESOURCE)

    def _parse_report(self, report: Report) -> ShortReport:
        """
        Parse the report produced by frictionless.
        """
        short_report = self._get_short_report()
        if len(report.tables) > 0:
            short_report.time = report.tables[0]["time"]
            short_report.valid = report.tables[0]["valid"]
            short_report.errors = report.tables[0]["errors"]

        return short_report

    def log_short_report(self, report: Report) -> None:
        """
        Method to log short report.
        """
        if not isinstance(report, Report):
            raise TypeError("Only frictionless report accepted.")

        report_short = self._parse_report(report)
        metadata = self._get_content(report_short.to_dict())
        self._log_metadata(metadata, self._SHORT_REPORT)

    def _log_metadata(self,
                      metadata: dict,
                      src_type: str) -> None:
        """
        Method to log generic metadata.
        """
        self._client._persist_metadata(
                            metadata,
                            self._run_info.run_metadata_uri,
                            src_type,
                            self._overwrite)

    def persist_artifact(self,
                         src: Any,
                         src_name: Optional[str] = None) -> None:
        """
        Method to persist artifacts in the artifact store.
        """
        file, uri = self._client._persist_artifact(
                                        src,
                                        self._run_info.run_artifacts_uri,
                                        src_name=src_name)
        metadata = self._get_content()
        metadata.pop("contents")
        metadata["name"] = file
        metadata["uri"] = uri
        self._log_metadata(metadata, self._ARTIFACT_METADATA)

    def persist_data(self) -> None:
        """
        Shortcut to persist data and validation schema.
        """
        self.persist_artifact(self._data_resource.path)
        if self._data_resource.schema is not None:
            self.persist_artifact(self._data_resource.schema)

    def persist_full_report(self, report: Report) -> None:
        """
        Shortcut to persist the full report produced
        by frictionless.
        """
        self.persist_artifact(
                    dict(report),
                    src_name=FileNames.FULL_REPORT.value)

    def persist_inferred_schema(self, schema: Schema) -> None:
        """
        Shortcut to persist the inferred schema produced
        by frictionless.
        """
        self.persist_artifact(
                    dict(schema),
                    src_name=FileNames.SCHEMA_INFERRED.value)

    def get_resource(self, **kwargs) -> Resource:
        """
        Return a frictionless Resource object.
        """
        if "path" in kwargs.keys():
            kwargs.pop("path")
        return Resource(path=self._data_resource.path,
                        **kwargs)
