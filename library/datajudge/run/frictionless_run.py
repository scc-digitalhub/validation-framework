"""
FrictionlessRun module.
Implementation of a Run object that uses Frictionless as
validation framework.
"""
from collections import namedtuple
from typing import Optional, Tuple

try:
    import frictionless
    from frictionless import Resource
    from frictionless.report import Report
    from frictionless.schema import Schema
except ImportError as ierr:
    raise ImportError("Please install frictionless!") from ierr

from datajudge.run import Run
from datajudge.utils.utils import guess_mediatype, warn


LIB_NAME = frictionless.__name__
LIB_VERSION = frictionless.__version__


class FrictionlessRun(Run):
    """
    Frictionless flavoured run.

    Methods
    -------
    build_frictionless_resource :
        Return a frictionless Resource object.
    build_frictionless_schema :
        Return a frictionless Schema object.

    """

    # Run

    def _update_library_info(self) -> None:
        """
        Update run's info about the validation framework used.
        """
        self.run_info.validation_library_name = LIB_NAME
        self.run_info.validation_library_version = LIB_VERSION

    # Data Resource

    def _update_data_resource(self) -> None:
        """
        Update resource with inferred information.
        """
        inferred = self.infer_resource()

        # Profile, format, encoding
        for key in ["profile", "format", "encoding"]:
            value = inferred.get(key)
            setattr(self.data_resource, key, value)

        # Bytes, MD5 Hash
        for key in ["bytes", "hash"]:
            value = inferred.get("stats", {}).get(key)
            setattr(self.data_resource, key, value)

        # Mediatype
        medtype = guess_mediatype(self.data_resource.path)
        self.data_resource.mediatype = medtype

    # Short Report

    def _parse_report(self,
                      nmtp: namedtuple) -> namedtuple:
        """
        Parse the report produced by frictionless.
        """
        duration = self.report.get("time")
        valid = self.report.get("valid")
        spec = ["fieldName", "rowNumber", "code", "note", "description"]
        flat_report = self.report.flatten(spec=spec)
        errors = [dict(zip(spec, err)) for err in flat_report]

        # error severity mapping

        return nmtp(LIB_NAME, LIB_VERSION, duration, valid, errors)

    def _check_report(self,
                      report: Optional[Report] = None) -> None:
        """
        Validate frictionless report before log/persist it.
        """
        if report is not None and not isinstance(report, Report):
            raise TypeError("Expected frictionless Report!")

    # Short Schema

    def _parse_schema(self,
                      nmtp: namedtuple) -> list:
        """
        Parse an inferred schema and return a standardized
        ShortSchema.
        """
        if self.inf_schema is None:
            return [nmtp("", "", "")]

        # Can be empty dict!
        self.fetch_validation_schema()
        schema = self.build_frictionless_schema(descriptor=self._val_schema)
        column_list = schema.get("fields", [])

        fields_list = []
        for field in self.inf_schema.get("fields", {}):

            name = field.get("name", "")
            type_ = field.get("type", "")

            for i in column_list:
                if name == i.get("name"):
                    valid_type = i.get("type", "")
                    desc = i.get("description", "")
                    break
            else:
                valid_type = ""
                desc = ""

            fields_list.append(nmtp(name, type_,
                                    valid_type, desc))

        return fields_list, LIB_NAME, LIB_VERSION

    def _check_schema(self,
                      schema: Optional[Schema] = None) -> None:
        """
        Validate frictionless schema before log/persist it.
        """
        if schema is not None and not isinstance(schema, Schema):
            raise TypeError("Expected frictionless schema!")

    # Framework wrapper methods

    def infer_schema(self) -> Schema:
        """
        Method that call infer on a frictionless Resource
        and return an inferred schema.
        """
        resource = self.infer_resource()
        schema = resource.get("schema")
        if schema is None:
            warn("Unable to infer schema.")
        return schema

    def infer_resource(self) -> Resource:
        """
        Infer on resource.
        """
        data_path = self.fetch_input_data()
        resource = self.build_frictionless_resource(path=data_path)
        resource.infer(stats=True)
        resource.expand()
        return resource

    def validate_resource(self, **kwargs: dict) -> Report:
        """
        Validate a Data Resource.

        Parameters
        ----------
        **kwargs : dict
            Keywords args for frictionless.validate_resource method.

        """
        schema_path = self.fetch_validation_schema()
        schema = self.build_frictionless_schema(descriptor=schema_path)
        if schema is None:
            warn("No validation schema is provided! " +
                 "Report will results valid by default.")

        data_path = self.fetch_input_data()
        resource = self.build_frictionless_resource(path=data_path,
                                                    schema=schema)
        report = frictionless.validate_resource(resource, **kwargs)

        return report

    def _parse_inference(self) -> Tuple[str, dict]:
        """
        Parse frictionless inferred resource and return file
        format and optional arguments for pandas.
        """

        pandas_args = {}

        if self.inferred is None:
            self.inferred = self.infer_resource()

        file_format = self.inferred.get("format")

        # Default args for read_csv: sep ",", encoding "utf-8"
        if file_format == "csv":
            pandas_args["sep"] = self.inferred.get("dialect", {})\
                                              .get("delimiter", ",")
            pandas_args["encoding"] = self.inferred.get("encoding", "utf-8")

        return file_format, pandas_args

    # Framework resources

    @staticmethod
    def build_frictionless_schema(**kwargs: dict) -> Schema:
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
        return Schema(**kwargs)

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
