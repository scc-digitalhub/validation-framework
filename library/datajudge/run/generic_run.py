"""
GenericRun module.
Implementation of a Run object that can do basic
task as logging metrics and persist artifacts.
"""
from __future__ import annotations

from typing import List, Optional

from datajudge.data import SchemaTuple
from datajudge.run import Run


class GenericRun(Run):
    """
    Generic flavoured run.

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

    """

    def _update_library_info(self) -> None:
        """
        Update run's info about the validation framework used.
        """

    def _update_data_resource(self) -> None:
        """
        Update resource with inferred information.
        """

    @staticmethod
    def _parse_report(report: dict, kwargs: dict) -> dict:
        """
        Parse the report.
        """
        for key in kwargs:
            try:
                kwargs[key] = report[key]
            except KeyError:
                continue
        return kwargs

    def _check_report(self, report: Optional[dict] = None) -> None:
        """
        Validate report before log/persist it.
        """
        if report is not None and not isinstance(report, dict):
            raise TypeError("Must be a dictionary!")
        elif report is None and self._report is None:
            raise TypeError("Provide a non empty valid dictionary!")

    @staticmethod
    def _infer_schema() -> None:
        """
        Method that call infer on a frictionless Resource
        and return an inferred schema.
        """
        return

    @staticmethod
    def _parse_schema(schema: dict) -> List[SchemaTuple]:
        """
        Parse an inferred schema and return a standardized
        ShortSchema.
        """
        return [SchemaTuple(f["name"], f["type"]) for f in schema["fields"]]

    def _check_schema(self, schema: Optional[dict] = None) -> None:
        """
        Validate schema before log/persist it.
        """
        if schema is not None and not isinstance(schema, dict):
            raise TypeError("Must be a dictionary!")
        if schema is not None and "fields" not in schema:
            raise KeyError("Malformed dictionary!")
        if schema is None and self._schema is None:
            raise TypeError("Provide a non empty valid dictionary!")
