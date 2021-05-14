"""
GenericRun module.
Implementation of a Run object that can do basic tasks
as logging metadata and persist artifacts.
"""
from collections import namedtuple
from typing import List, Optional

from datajudge.run import Run
from datajudge.utils.utils import guess_mediatype


class GenericRun(Run):
    """
    Generic flavoured run.
    Used for tasks such metadata logging and artifacts persistence.
    Do not use it without passing reports/profiles/schemas to its
    methods.

    """

    # Run

    def _update_library_info(self) -> None:
        """
        Update run's info about the validation framework used.
        """
        self.run_info.validation_library = "-"
        self.run_info.library_version = "-"

    # Data Resource

    def _update_data_resource(self) -> None:
        """
        Update resource with inferred information.
        """
        # Mediatype
        self.data_resource.mediatype = guess_mediatype(self.data_resource.path)

    # Short Report

    def _parse_report(self,
                      nmtp: namedtuple) -> namedtuple:
        """
        Parse the report.
        """
        try:
            valid = self.report["valid"]
            time = self.report["time"]
            errors = self.report["errors"]
        except KeyError:
            valid, time, errors = None, None, None
        return nmtp(valid, time, errors)

    def _check_report(self,
                      report: Optional[dict] = None) -> None:
        """
        Validate report before log/persist it.
        """
        if report is not None and not isinstance(report, dict):
            raise TypeError("Must be a dictionary!")
        if report is None and self.report is None:
            raise TypeError("Provide a non empty valid dictionary!")

    # Short Schema

    def _parse_schema(self,
                      nmtp: namedtuple) -> List[namedtuple]:
        """
        Parse an inferred schema.
        """
        if self.inf_schema is None:
            return [nmtp("", "")]
        return [nmtp(f["name"], f["type"]) for f in self.inf_schema["fields"]]

    def _check_schema(self,
                      schema: Optional[dict] = None) -> None:
        """
        Validate schema before log/persist it.
        """
        if schema is not None and not isinstance(schema, dict):
            raise TypeError("Must be a dict!")

        # Basically we accept a frictionless like schema
        if schema is not None and "fields" not in schema:
            raise KeyError("Provide a dict with 'fields' key.")

        if isinstance(schema["fields"], list):
            for i in schema["fields"]:
                if "name" not in i and "type" not in i:
                    raise KeyError("Provide a dict with 'name' ",
                                   "and 'type' keys.")
        else:
            raise TypeError("Must be a list of dict!")

    # Framework wrapper methods

    def infer_schema(self) -> None:
        raise TypeError("Cannot perform inference with generic run.")

    def infer_resource(self) -> None:
        raise TypeError("Cannot perform inference with generic run.")

    def validate_resource(self) -> None:
        raise TypeError("Cannot perform validation with generic run.")

    def _parse_inference(self) -> None:
        raise TypeError("Cannot perform inference with generic run.")
