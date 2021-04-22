"""
FrictionlessRun module.
Implementation of a Run object that uses Frictionless as
validation framework.
"""
from __future__ import annotations

from mimetypes import guess_type
from typing import List, Optional

try:
    import frictionless
    from frictionless import Resource, validate_resource
    from frictionless.exception import FrictionlessException
    from frictionless.report import Report
    from frictionless.schema import Schema
except ImportError as ierr:
    raise ImportError("Please install frictionless!") from ierr

from datajudge.data import SchemaTuple
from datajudge.run import Run


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

    # Run

    def _update_library_info(self) -> None:
        """
        Update run's info about the validation framework used.
        """
        self.run_info.validation_library = frictionless.__name__
        self.run_info.library_version = frictionless.__version__

    # DataResource

    def _update_data_resource(self) -> None:
        """
        Update resource with inferred information.
        """
        frict_res = self._infer_resource()
        try:
            for key in ["profile", "format", "encoding"]:
                setattr(self.data_resource, key, frict_res[key])
            for key in ["bytes", "hash"]:
                setattr(self.data_resource, key, frict_res["stats"][key])
            if isinstance(self.data_resource.path, str):
                mediatype, _ = guess_type(self.data_resource.path)
            else:
                # Apparently frictionless fetch the first file and
                # generalize the inference to all the other files
                # e.g. if the first file is a csv and the second a
                # tsv, for the data resource all of them are csv.
                mediatype, _ = guess_type(self.data_resource.path[0])
            self.data_resource.mediatype = mediatype

        except KeyError as kex:
            raise kex

    # Short report

    @staticmethod
    def _parse_report(report: Report, kwargs: dict) -> dict:
        """
        Parse the report produced by frictionless.
        """
        if len(report.tables) > 0:
            for key in kwargs:
                kwargs[key] = report.tables[0][key]
        return kwargs

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
        resource = self._infer_resource()
        return resource["schema"]

    # Short schema

    @staticmethod
    def _parse_schema(schema: Schema) -> List[SchemaTuple]:
        """
        Parse an inferred schema and return a standardized
        ShortSchema.
        """
        return [SchemaTuple(f["name"], f["type"]) for f in schema["fields"]]

    @staticmethod
    def _check_schema(schema: Optional[Schema] = None) -> None:
        """
        Validate frictionless schema before log/persist it.
        """
        if schema is not None and not isinstance(schema, Schema):
            raise TypeError("Expected frictionless schema!")

    # Build frictionless objects

    @staticmethod
    def build_frictionless_schema(schema: dict) -> Schema:
        """
        Get frictionless schema object.
        """
        return Schema(schema)

    def build_frictionless_resource(self,
                                    from_path: bool = False,
                                    **kwargs
                                    ) -> Resource:
        """
        Return a frictionless Resource object.

        Parameters
        ----------
        from_path : bool, default = False
            If True, build a frictionless resource from
            DataResource path.
        kwargs : dict, default = None
            Arguments to pass to frictionless Resource
            constructor.

        Returns
        -------
        Resource

        """
        if from_path:
            kwargs["path"] = self.data_resource.path
        return Resource(**kwargs)

    # Framework wrapper methods

    def _infer_resource(self) -> Resource:
        """
        Infer on resource.
        """
        try:
            resource = self.build_frictionless_resource(
                                            from_path=True)
            resource.infer()

        except FrictionlessException:

            data = self.fetch_input_data(cached=True)
            resource = self.build_frictionless_resource(data=data)
            resource.infer()

        resource.expand()
        return resource

    def validate_resource(self) -> Report:
        """
        Validate a Data Resource.
        """
        if self.data_resource.schema is None:
            raise RuntimeError("No validation schema provided!")

        schema = self.fetch_validation_schema(cached=True)
        schema = self.build_frictionless_schema(schema)

        try:
            resource = self.build_frictionless_resource(from_path=True,
                                                        schema=schema)
            report = validate_resource(resource)

        except FrictionlessException:

            data = self.fetch_input_data(cached=True)
            resource = self.build_frictionless_resource(data=data,
                                                        schema=schema)
            report = validate_resource(resource)

        return report
