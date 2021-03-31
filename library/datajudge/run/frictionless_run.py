from __future__ import annotations

import typing
from mimetypes import guess_type
from typing import Any, List, Optional, Union

import frictionless
from datajudge.run import Run
from frictionless import Resource
from frictionless.report import Report
from frictionless.schema import Schema

if typing.TYPE_CHECKING:
    from datajudge.client import Client
    from datajudge.data import DataResource, ShortReport
    from datajudge.run import RunInfo


class FrictionlessRun(Run):
    """
    Frictionless flavoured run.

    See also
    --------
    Run : Abstract run class.

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
        self.run_info.validation_library = frictionless.__name__
        self.run_info.library_version = frictionless.__version__

    def _update_data_resource(self) -> None:
        """
        Update resource with inferred information.
        """
        frict_resource = self.get_resource()
        frict_resource.infer()
        try:
            self.data_resource._profile = frict_resource["profile"]
            self.data_resource._format = frict_resource["format"]
            if isinstance(self.data_resource.path, str):
                mediatype, _ = guess_type(self.data_resource.path)
            else:
                # Apparently frictionless fetch the first file and
                # generalize the inference to all the other files
                # e.g. if the first file is a csv and the second a
                # tsv, for the data resource all of them are csv.
                mediatype, _ = guess_type(self.data_resource.path[0])
            mediatype = mediatype if mediatype is not None else ""
            self.data_resource._mediatype = mediatype
            self.data_resource._encoding = frict_resource["encoding"]
            self.data_resource._bytes = frict_resource["stats"]["bytes"]
            self.data_resource._hash = frict_resource["stats"]["hash"]
        except KeyError as kex:
            raise kex

    def _log_run(self) -> None:
        """
        Method to log run's metadata.
        """
        metadata = self._get_content(self.run_info.to_dict())
        self._log_metadata(metadata, self._RUN_METADATA)

    def log_data_resource(self) -> None:
        """
        Method to log data resource.
        """
        metadata = self._get_content(self.data_resource.to_dict())
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

        Parameters
        ----------
        report : Report
            A frictionless Report object.

        """
        if not isinstance(report, Report):
            raise TypeError("Only frictionless report accepted.")

        report_short = self._parse_report(report)
        metadata = self._get_content(report_short.to_dict())
        self._log_metadata(metadata, self._SHORT_REPORT)

    def _log_artifact(self,
                      src: Any,
                      src_name: Optional[str] = None
                      ) -> None:
        """
        Method to log artifacts metadata.
        """
        uri = self.run_info.run_artifacts_uri
        names = []
        if isinstance(src, list):
            names.extend(src)
        elif isinstance(src, str):
            names.append(src)
        else:
            names.append(src_name)

        for name in names:
            metadata = self._get_artifact_metadata(name, uri)
            self._log_metadata(metadata, self._ARTIFACT_METADATA)

    def _log_metadata(self,
                      metadata: dict,
                      src_type: str) -> None:
        """
        Method to log generic metadata.
        """
        self.client.log_metadata(
                           metadata,
                           self.run_info.run_metadata_uri,
                           src_type,
                           self._overwrite)

    def persist_artifact(self,
                         src: Union[str, List[str], dict],
                         src_name: Optional[str] = None
                         ) -> None:
        """
        Method to persist artifacts in the artifact store.

        Parameters
        ----------
        src : str, list or dict
            One or a list of URI described by a string, or a dictionary.
        src_name : str, default = None
            Filename. Required only if src is a dictionary.

        """
        self.client.persist_artifact(src,
                                     self.run_info.run_artifacts_uri,
                                     src_name=src_name)
        self._log_artifact(src, src_name)

    def persist_data(self) -> None:
        """
        Shortcut to persist data and validation schema.
        """
        self.persist_artifact(self.data_resource.path)
        if self.data_resource.schema is not None:
            self.persist_artifact(self.data_resource.schema)

    def persist_full_report(self, report: Report) -> None:
        """
        Shortcut to persist the full report produced
        by frictionless.

        Parameters
        ----------
        report : Report
            A frictionless Report object.

        """
        self.persist_artifact(
                    dict(report),
                    src_name=self._FULL_REPORT)

    def persist_inferred_schema(self, schema: Schema) -> None:
        """
        Shortcut to persist the inferred schema produced
        by frictionless.

        Parameters
        ----------
        schema : Schema
            A frictionless Schema object.

        """
        self.persist_artifact(
                    dict(schema),
                    src_name=self._SCHEMA_INFERRED)

    def get_resource(self, **kwargs) -> Resource:
        """
        Return a frictionless Resource object.

        Parameters
        ----------
        kwargs : dict
            Optional arguments to pass to frictionless Resource
            constructor.

        Returns
        -------
        Resource

        """
        if "path" in kwargs.keys():
            kwargs.pop("path")
        return Resource(path=self.data_resource.path,
                        **kwargs)
