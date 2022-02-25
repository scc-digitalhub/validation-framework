"""
Frictionless implementation of validation plugin.
"""
# pylint: disable=import-error,invalid-name
import warnings
from typing import List, Optional

import frictionless
from frictionless import Report, Resource, Schema

from datajudge.run.plugin.validation.validation_plugin import Validation


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
                     report: Report
                     ) -> tuple:
        """
        Parse the report produced by frictionless.
        """
        duration = report.get("time")
        valid = report.get("valid")
        spec = ["fieldName", "rowNumber", "code", "note", "description"]
        flat_report = report.flatten(spec=spec)
        errors = [dict(zip(spec, err)) for err in flat_report]
        return self.get_report_tuple(duration, valid, errors)

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
                 valid_kwargs: Optional[dict] = None) -> Report:
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

        valid_kwargs = self.get_args(valid_kwargs)

        try:
            schema = Schema(constraints)
        except Exception:
            warnings.warn("Invalid constraints format.")
        finally:
            schema = Schema(descriptor=schema_path)

        if not schema or schema is None:
            warnings.warn("No valid table schema is provided! " +
                          "Report will results valid by default.")

        resource = Resource(path=data_path, schema=schema)
        report = frictionless.validate_resource(resource, **valid_kwargs)
        end = report.time

        self.registry.add_result(res_name, report, end)

        return report

    @staticmethod
    def get_outcome(obj: Report) -> str:
        """
        Return status of the execution.
        """
        if obj.get("valid", False):
            return "valid"
        return "invalid"

    def render_artifact(self,
                        obj: Report) -> List[tuple]:
        """
        Return a rendered profile ready to be persisted as artifact.
        """
        self.validate_report(obj)
        report = dict(obj)
        filename = self._fn_report.format("frictionless.json")
        return [self.get_render_tuple(report, filename)]
