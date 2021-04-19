"""
FrictionlessRun module.
Implementation of a Run object that uses Frictionless as
validation framework.
"""
from __future__ import annotations

import typing
from mimetypes import guess_type
from typing import Optional

try:
    import frictionless
    from frictionless import Resource
    from frictionless.report import Report
    from frictionless.schema import Schema
except ImportError as ierr:
    raise ImportError("Please install frictionless!") from ierr

from datajudge.data import SchemaTuple
from datajudge.run import Run

if typing.TYPE_CHECKING:
    from datajudge.data import ShortReport, ShortSchema


class FrictionlessRun(Run):
    """
    Frictionless flavoured run.

    Methods
    -------
    log_data_resource :
        Method to log data resource.
    log_short_report :
        Method to log short report.
    log_short_schema :
        Method to log short schema.
    persist_data :
        Shortcut to persist data and validation schema.
    persist_full_report :
        Shortcut to persist the full report produced by the validation
        framework as artifact.
    persist_inferred_schema :
        Shortcut to persist the inferred schema produced by the
        validation framework as artifact.
    persist_artifact :
        Method to persist artifacts in the artifact store.

    See also
    --------
    Run : Abstract run class.

    """

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
        frict_resource = self.get_frictionless_resource()
        frict_resource.infer()
        res = self.data_resource
        try:
            res.profile = frict_resource["profile"]
            res.format = frict_resource["format"]
            if isinstance(res.path, str):
                mediatype, _ = guess_type(res.path)
            else:
                # Apparently frictionless fetch the first file and
                # generalize the inference to all the other files
                # e.g. if the first file is a csv and the second a
                # tsv, for the data resource all of them are csv.
                mediatype, _ = guess_type(res.path[0])
            mediatype = mediatype if mediatype is not None else ""
            res.mediatype = mediatype
            res.encoding = frict_resource["encoding"]
            res.bytes = frict_resource["stats"]["bytes"]
            res.hash = frict_resource["stats"]["hash"]
        except KeyError as kex:
            raise kex

        # Cleanup
        del frict_resource

    def _parse_report(self, report: Report) -> ShortReport:
        """
        Parse the report produced by frictionless.
        """
        short_report = self._create_short_report()
        if len(report.tables) > 0:
            short_report.time = report.tables[0]["time"]
            short_report.valid = report.tables[0]["valid"]
            short_report.errors = report.tables[0]["errors"]

        return short_report

    @staticmethod
    def _check_report(report: Optional[Report] = None) -> None:
        """
        Validate frictionless report before log/persist it.
        """
        if report is not None and not isinstance(report, Report):
            raise TypeError("Expected frictionless Report!")

    def _infer_schema(self) -> Schema:
        """
        Method that call infer on a frictionless Resource
        and return an inferred schema.
        """
        resource = self.get_frictionless_resource()
        resource.infer()
        return resource["schema"]

    def _parse_schema(self, schema: Schema) -> ShortSchema:
        """
        Parse an inferred schema and return a standardized
        ShortSchema.
        """
        parsed = [SchemaTuple(f["name"], f["type"]) for f in schema["fields"]]
        short_schema = self._create_short_schema(parsed)
        return short_schema

    @staticmethod
    def _check_schema(schema: Optional[Schema] = None) -> None:
        """
        Validate frictionless schema before log/persist it.
        """
        if schema is not None and not isinstance(schema, Schema):
            raise TypeError("Expected frictionless schema!")

    def get_frictionless_resource(self, **kwargs) -> Resource:
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
        if "path" not in kwargs or "data" not in kwargs:
            kwargs["path"] = self.data_resource.path
        return Resource(**kwargs)
