"""
Frictionless implementation of validation plugin.
"""
# pylint: disable=import-error,invalid-name
from __future__ import annotations

import typing
from typing import List

import frictionless
from frictionless import Report, Resource, Schema

from datajudge.run.plugin.validation.validation_plugin import Validation

if typing.TYPE_CHECKING:
    from datajudge.utils.config import ConstraintsDatajudge


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

    def rebuild_constraint(self,
                           constraints: List[ConstraintsDatajudge]) -> None:
        """
        Rebuild input constraints.
        """
        resources = {}

        for con in constraints:
            resource = con.resources[0]
            if resource not in resources:
                resources[resource] = {}

        for res in resources:

            fields = {}
            schema = {
                "fields": []
            }

            for con in constraints:

                field_name = con.field
                val = con.value
                con_type = con.constraint

                if con.resources[0] == res:
                    if field_name not in fields:
                        fields[field_name] = {
                            "name": field_name,
                            "type": None,
                            "error": {
                                "severity": con.severity
                            },
                            "constraints": {}
                        }

                    if con_type == "Type":
                        fields[field_name]["type"] = val

                    elif con_type == "Format":
                        fields[field_name]["format"] = val

                    else:
                        fields[field_name]["constraints"][con_type] = val

            for _, con in fields.items():
                schema["fields"].append(con)

            self.registry.add_constraints(res, schema)

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
                 exec_args: dict) -> Report:
        """
        Validate a Data Resource.

        Parameters
        ----------
        **exec_args : dict
            Keywords args for frictionless.validate_resource method.

        """
        constraints = self.registry.get_constraints(res_name)
        schema = Schema(constraints)

        resource = Resource(path=data_path, schema=schema)
        report = frictionless.validate_resource(resource, **exec_args)
        end = report.time
        
        result = self.get_outcome(report)

        self.registry.add_result(res_name, report, result, end)

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
