"""
InferencePluginFrictionless module.
Implementation of a Run plugin that uses Frictionless as
validation framework.
"""

# pylint: disable=import-error,invalid-name
from __future__ import annotations

from typing import Optional

from datajudge.utils.utils import warn

try:
    import frictionless
    from frictionless import Report, Schema, Resource
except ImportError as ierr:
    raise ImportError("Please install frictionless!") from ierr

from datajudge.data import ReportTuple
from datajudge.run.validation.validation_plugin import Validation


class ValidationPluginFrictionless(Validation):
    """
    Run plugin that executes inference over a Resource.
    """

    def update_library_info(self) -> None:
        """
        Update run's info about the validation framework used.
        """
        self.lib_name = frictionless.__name__
        self.lib_version = frictionless.__version__

    def parse_report(self,
                     report: Report,
                     schema_path: Optional[str] = None
                     ) -> ReportTuple:
        """
        Parse the report produced by frictionless.
        """
        # Extract values from report
        duration = report.get("time")
        valid = report.get("valid")
        spec = ["fieldName", "rowNumber", "code", "note", "description"]
        flat_report = report.flatten(spec=spec)
        errors = [dict(zip(spec, err)) for err in flat_report]

        # Error severity mapping.
        # See documentation for the validation schema integration.       
        schema = Schema(descriptor=schema_path)
       
        if schema:
            val_fields = schema.get("fields")
            for err in errors:
                error_field = err.get("fieldName")
                for field in val_fields:
                    if field.get("name") == error_field:
                        err["severity"] = field.get("errors", {})\
                                               .get("severity", 5)
                        break

        return ReportTuple(duration, valid, errors)

    def validate_report(self,
                      report: Optional[Report] = None) -> None:
        """
        Validate frictionless report before log/persist it.
        """
        if report is not None and not isinstance(report, Report):
            raise TypeError("Expected frictionless Report!")

    def validate(self,
                 data_path: str,
                 schema_path: str,
                 kwargs: dict) -> Report:
        """
        Validate a Data Resource.

        Parameters
        ----------
        **kwargs : dict
            Keywords args for frictionless.validate_resource method.

        """
        if not kwargs:
            kwargs = {}
       
        schema = Schema(descriptor=schema_path)
        if schema is None:
            warn("No validation schema is provided! " +
                 "Report will results valid by default.")

        resource = Resource(path=data_path, schema=schema)
        report = frictionless.validate_resource(resource, **kwargs)

        return report
