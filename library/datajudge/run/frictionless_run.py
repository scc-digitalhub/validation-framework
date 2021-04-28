"""
FrictionlessRun module.
Implementation of a Run object that uses Frictionless as
validation framework.
"""
import warnings
from mimetypes import guess_type
from typing import List, Optional, Tuple

try:
    import frictionless
    from frictionless import Resource
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
        frict_res = self.infer_resource()
        try:
            for key in ["profile", "format", "encoding"]:
                setattr(self.data_resource, key, frict_res[key])
            if "stats" in frict_res:
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
        if not hasattr(report, "tasks"):
            return kwargs
        if len(report.tasks) > 0:
            for key in kwargs:
                kwargs[key] = report.tasks[0][key]
        return kwargs

    def _check_report(self, report: Optional[Report] = None) -> None:
        """
        Validate frictionless report before log/persist it.
        """
        if report is not None and not isinstance(report, Report):
            raise TypeError("Expected frictionless Report!")

    # Short schema

    @staticmethod
    def _parse_schema(schema: Schema) -> List[SchemaTuple]:
        """
        Parse an inferred schema and return a standardized
        ShortSchema.
        """
        if schema is None:
            new = [SchemaTuple("", "")]
        else:
            new = [SchemaTuple(f["name"], f["type"]) for f in schema["fields"]]
        return new

    def _infer_schema(self) -> Schema:
        """
        Method that call infer on a frictionless Resource
        and return an inferred schema.
        """
        resource = self.infer_resource()
        if "schema" in resource:
            return resource["schema"]
        # to change
        return

    @staticmethod
    def _check_schema(schema: Optional[Schema] = None) -> None:
        """
        Validate frictionless schema before log/persist it.
        """
        if schema is not None and not isinstance(schema, Schema):
            raise TypeError("Expected frictionless schema!")

    # Inferred resource

    def _parse_inference(self) -> Tuple[str, dict]:
        """
        Parse frictionless inferred resource.
        """
        if self._inferred is None:
            self.infer_resource()

        pandas_args = {
            "sep": ",",
            "encoding": "tf-8"
        }

        file_format = self._inferred["format"]
        if file_format == "csv":
            try:
                pandas_args["sep"] = self._inferred["dialect"]["delimiter"]
                pandas_args["encoding"] = self._inferred["encoding"]
            except KeyError:
                pass
        else:
            pandas_args = {}

        return file_format, pandas_args

    # Build frictionless objects

    @staticmethod
    def build_frictionless_schema(schema: dict) -> Schema:
        """
        Return a frictionless Schema object.

        Parameters
        ----------
        **kwargs : dict
            Arguments to pass to frictionless Schema constructor.

        Returns
        -------
        Schema

        """
        return Schema(schema)

    @staticmethod
    def build_frictionless_resource(**kwargs: dict) -> Resource:
        """
        Return a frictionless Resource object.

        Parameters
        ----------
        **kwargs : dict
            Arguments to pass to frictionless Resource constructor.

        Returns
        -------
        Resource

        """
        return Resource(**kwargs)

    # Framework wrapper methods

    def infer_resource(self) -> Resource:
        """
        Infer on resource.
        """
        data_path = self.fetch_input_data()
        resource = self.build_frictionless_resource(path=data_path)
        resource.infer()
        resource.expand()
        if self._inferred is None:
            self._inferred = resource
        return self._inferred

    def validate_resource(self, **kwargs: dict) -> Report:
        """
        Validate a Data Resource.

        Parameters
        ----------
        **kwargs : dict
            Keywords args for frictionless.validate_resource
            method.

        """
        schema = self.fetch_validation_schema()
        schema = self.build_frictionless_schema(schema)
        if schema is None:
            warnings.warn("No validation schema is provided! " +
                          "Report will results valid by default.")

        data_path = self.fetch_input_data()
        resource = self.build_frictionless_resource(path=data_path,
                                                    schema=schema)
        report = frictionless.validate_resource(resource, **kwargs)

        if self._report is None:
            self._report = report

        return report
