"""
Frictionless implementation of validation plugin.
"""
# pylint: disable=import-error,invalid-name
import warnings
from typing import List, Optional

import frictionless
from frictionless import Report, Resource, Schema

from datajudge.run.validation.validation_plugin import (RenderTuple,
                                                        ReportTuple,
                                                        Validation)


FN_REPORT = "report_frictionless.json"


class ValidationPluginFrictionless(Validation):
    """
    Frictionless implementation of validation plugin.
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
                        report: Report) -> None:
        """
        Validate frictionless report before log/persist it.
        """
        if not isinstance(report, Report):
            raise TypeError("Expected frictionless Report!")

    def validate(self,
                 res_name: str,
                 data_path: str,
                 constraints: Optional[dict] = None,
                 schema_path: Optional[str] = None,
                 kwargs: Optional[dict] = None) -> Report:
        """
        Validate a Data Resource.

        Parameters
        ----------
        **kwargs : dict
            Keywords args for frictionless.validate_resource method.

        """
        report = self.registry.get_result(res_name)
        if report is not None:
            return report
        
        if not kwargs:
            kwargs = {}

        try:
            schema = Schema(constraints)
        except:
            warnings.warn("Invalid constraints format.")
        finally:
            schema = Schema(descriptor=schema_path)

        if not schema or schema is None:
            warnings.warn("No valid table schema is provided! " +
                 "Report will results valid by default.")

        resource = Resource(path=data_path, schema=schema)
        report = frictionless.validate_resource(resource, **kwargs)
        end = report.time
        
        self.registry.add_result(res_name, report, end)

        return report

    def render_object(self,
                      obj: Report) -> List[RenderTuple]:
        """
        Return a rendered profile ready to be persisted as artifact.
        """

        self.validate_report(obj)
        dict_report = dict(obj)

        return [RenderTuple(dict_report, FN_REPORT)]
