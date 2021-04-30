"""
Interface for specific library runs.
"""
# pylint: disable=import-error,invalid-name
from __future__ import annotations

import json
import typing
import warnings
from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List, Optional, Tuple, Union

import pandas as pd
from pandas_profiling import ProfileReport
from datajudge.data import ShortReport, ShortSchema
from datajudge.utils import config as cfg
from datajudge.utils.file_utils import clean_all
from datajudge.utils.io_utils import write_bytesio
from datajudge.utils.time_utils import get_time
from datajudge.utils.uri_utils import get_name_from_uri
from datajudge.utils.utils import data_listify

if typing.TYPE_CHECKING:
    from datajudge.client import Client
    from datajudge.data import DataResource
    from datajudge.run import RunInfo

# pylint: disable=too-many-instance-attributes


class Run:
    """
    Run abstract object.
    The run is the main interface to interact with data and metadata.
    It interacts both with the Client and the Data Resource/Package.

    Attributes
    ----------
    run_info : RunInfo
        The metadata info of the run.
    data_resource : DataResource
        A DataResource object.
    client : Client
        A Client object that interact with the storages.

    Methods
    -------
    get_run :
        Return Run Info as dictionary.

    """

    __metaclass__ = ABCMeta

    _RUN_METADATA = cfg.MT_RUN_METADATA
    _DATA_RESOURCE = cfg.MT_DATA_RESOURCE
    _SHORT_REPORT = cfg.MT_SHORT_REPORT
    _SHORT_SCHEMA = cfg.MT_SHORT_SCHEMA
    _DATA_PROFILE = cfg.MT_DATA_PROFILE
    _ARTIFACT_METADATA = cfg.MT_ARTIFACT_METADATA

    _VALID_SCHEMA = cfg.FN_VALID_SCHEMA
    _FULL_REPORT = cfg.FN_FULL_REPORT
    _SCHEMA_INFERRED = cfg.FN_INFERRED_SCHEMA
    _FULL_PROFILE = cfg.FN_FULL_PROFILE

    def __init__(self,
                 run_info: RunInfo,
                 data_resource: DataResource,
                 client: Client,
                 overwrite: bool) -> None:

        self._data_resource = data_resource
        self._client = client
        self.run_info = run_info
        self._overwrite = overwrite

        # Local temp paths
        self._data = None
        self._val_schema = None

        # Cahcing results of inference/validation/profiling
        self._inferred = None
        self._inf_schema = None
        self._report = None
        self._profile = None

        self._update_library_info()
        self._log_run()

    # Run metadata

    @abstractmethod
    def _update_library_info(self) -> None:
        """
        Update run's info about the validation framework used.
        """

    def _log_run(self) -> None:
        """
        Method to log run's metadata.
        """
        metadata = self._get_content(self.run_info.to_dict())
        self._log_metadata(metadata, self._RUN_METADATA)

    # DataResource

    @abstractmethod
    def _update_data_resource(self) -> None:
        """
        Update resource with inferred information.
        """

    def log_data_resource(self,
                          infer: bool = False) -> None:
        """
        Method to log data resource.

        Parameters
        ----------
        infer : bool, default = False
            Options to make inference on data resource.

        """
        if infer:
            self._update_data_resource()
        metadata = self._get_content(self.data_resource.to_dict())
        self._log_metadata(metadata, self._DATA_RESOURCE)

        # Update run info
        if self.run_info.data_resource_uri is None:
            uri_resource = self._client.get_data_resource_uri(
                                                self.run_info.run_id)
            self.run_info.data_resource_uri = uri_resource

    # Short report

    @staticmethod
    def _create_short_report(kwargs: dict) -> ShortReport:
        """
        Return a ShortReport object.
        """
        return ShortReport(**kwargs)

    @abstractmethod
    def _parse_report(self,
                      report: Any, kwargs: dict) -> dict:
        """
        Parse the report produced by the validation framework.
        """

    def _set_report(self,
                    report: Optional[Any] = None,
                    infer: bool = False) -> None:
        """
        Set private attribute 'report'.
        """
        if self._report is None:
            if report is None and infer:
                self._report = self.validate_resource()
            else:
                self._report = report

    @abstractmethod
    def _check_report(self,
                      report: Any) -> None:
        """
        Check a report before log/persist it.
        """

    def log_short_report(self,
                         report: Optional[dict] = None,
                         infer: bool = False) -> None:
        """
        Method to log short report.

        Parameters
        ----------
        report : Any
            A report object to be logged. If it is not
            provided, the run will check its own report attribute.
        infer : bool, default = True
            If True, try to infer schema from resource.

        """
        self._check_report(report)
        self._set_report(report, infer)

        report_args = {
            "time": None,
            "valid": None,
            "errors": None
        }

        if self._report is not None:
            report_args = self._parse_report(self._report, report_args)

        report_args["data_resource"] = self.run_info.data_resource_uri
        report_args["experiment_name"] = self.run_info.experiment_name
        report_args["run_id"] = self.run_info.run_id

        short_schema = self._create_short_report(report_args)

        metadata = self._get_content(short_schema.to_dict())
        self._log_metadata(metadata, self._SHORT_REPORT)

    # Short schema

    @abstractmethod
    def _infer_schema(self) -> Any:
        """
        Parse the inferred schema produced by the validation
        framework.
        """

    @staticmethod
    def _create_short_schema(fields: List[Dict[str, str]]
                             ) -> ShortSchema:
        """
        Return a ShortSchema object.
        """
        return ShortSchema(fields)

    @abstractmethod
    def _parse_schema(self,
                      schema: Any) -> ShortSchema:
        """
        Parse the inferred schema produced by the validation
        framework.
        """

    def _set_schema(self,
                    schema: Optional[Any] = None,
                    infer: bool = False) -> None:
        """
        Set private attribute 'inferred schema'.
        """
        if self._inf_schema is None:
            if schema is None and infer:
                self._inf_schema = self._infer_schema()
            else:
                self._inf_schema = schema

    @abstractmethod
    def _check_schema(self,
                      schema: Any) -> None:
        """
        Check a schema before log/persist it.
        """

    def log_short_schema(self,
                         schema: Optional[dict] = None,
                         infer: bool = False) -> dict:
        """
        Method to log short schema.

        Parameters
        ----------
        schema : Schema, default = None
            An inferred schema to be logged. If it is not
            provided, the run will check its own schema attribute.
        infer : bool, default = True
            If True, try to infer schema from resource.

        """
        self._check_schema(schema)
        self._set_schema(schema, infer)

        if self._inf_schema is not None:
            parsed = self._parse_schema(self._inf_schema)

            short_schema = self._create_short_schema(parsed)
            metadata = self._get_content(short_schema.to_dict())

            self._log_metadata(metadata, self._SHORT_SCHEMA)

    # Data profile

    @staticmethod
    def _parse_profile(profile: ProfileReport) -> dict:
        """
        Parse the profile generated by pandas profiling.
        """
        dict_ = json.loads(profile.to_json())
        keys = [k for k in ["analysis", "table", "package"] if k in dict_]
        short_profile = {k: dict_[k] for k in keys}
        return short_profile

    def _check_profile(self,
                       profile: Optional[ProfileReport] = None
                       ) -> ProfileReport:
        """
        Check validity of profile.
        """
        if profile is None:
            if self.profile is None:
                raise RuntimeError("No profile provided, skipping!")
            return self.profile

        if profile is not None and not isinstance(profile, ProfileReport):
            raise TypeError("Expected frictionless Report!")

        return profile

    def log_profile(self,
                    profile: Optional[ProfileReport] = None
                    ) -> None:
        """
        Method to log a pandas profile.
        """
        to_parse = self._check_profile(profile)
        parsed = self._parse_profile(to_parse)
        metadata = self._get_content(parsed)
        self._log_metadata(metadata, self._DATA_PROFILE)

    @abstractmethod
    def _parse_inference(self) -> Tuple[str, dict]:
        """
        Method to parse inference from specific
        validation framework.
        """

    @staticmethod
    def _read_df(path: Union[str, List[str]],
                 file_format: str,
                 **kwargs: dict) -> pd.DataFrame:
        """
        Read a file into a pandas DataFrame.
        """

        # Check if path is a list
        is_list = False
        if isinstance(path, list):
            is_list = True

        if file_format == "csv":
            if is_list:
                list_df = [pd.read_csv(i, **kwargs) for i in path]
                df = pd.concat(list_df)
            else:
                df = pd.read_csv(path, **kwargs)

        if file_format in ["xls", "xlsx"]:
            if is_list:
                list_df = [pd.read_excel(i, **kwargs) for i in path]
                df = pd.concat(list_df)
            else:
                df = pd.read_excel(path, **kwargs)

        return df

    def generate_profile(self,
                         **kwargs: dict) -> None:
        """
        Method to generate profile.

        Parameters
        ----------
        **kwargs : dict
            Parameters for pandas_profiling.ProfileReport.

        """
        file_format, pandas_kwargs = self._parse_inference()
        df = self._read_df(self.fetch_input_data(),
                           file_format,
                           **pandas_kwargs)
        profile = ProfileReport(df, **kwargs)
        self._profile = profile

    # Artifact metadata

    def _get_artifact_metadata(self,
                               uri: str,
                               name: str) -> dict:
        """
        Build artifact metadata.
        """
        metadata = self._get_content()
        metadata.pop("contents")
        metadata["uri"] = uri
        metadata["name"] = name
        return metadata

    def _log_artifact(self,
                      src_name: Optional[str] = None
                      ) -> None:
        """
        Method to log artifact metadata.
        """
        uri = self.run_info.run_artifacts_uri
        metadata = self._get_artifact_metadata(uri, src_name)
        self._log_metadata(metadata, self._ARTIFACT_METADATA)

    # Metadata

    def _get_content(self,
                     cont: Optional[dict] = None) -> dict:
        """
        Return structured content to log.
        """
        content = {
            "run_id": self.run_info.run_id,
            "experiment_id": self.run_info.experiment_id,
            "experiment_name": self.run_info.experiment_name,
            "contents": cont
        }
        return content

    def _log_metadata(self,
                      metadata: dict,
                      src_type: str) -> None:
        """
        Method to log generic metadata.
        """
        self._client.log_metadata(
                           metadata,
                           self.run_info.run_metadata_uri,
                           src_type,
                           self._overwrite)

    # Input data

    def fetch_validation_schema(self) -> str:
        """
        Fetch validation schema from backend and return temp file path.
        """
        if self.data_resource.schema is None:
            return None
        if self._val_schema is None:
            self._val_schema = self.fetch_artifact(self.data_resource.schema)
        return self._val_schema

    def fetch_input_data(self) -> str:
        """
        Fetch data from backend and return temp file path.
        """
        if self._data is None:
            path = self.data_resource.path
            if isinstance(path, list):
                self._data = [self.fetch_artifact(i) for i in path]
            else:
                self._data = self.fetch_artifact(path)
        return self._data

    def fetch_artifact(self,
                       uri: str) -> str:
        """
        Method to fetch artifact from backend.

        Parameters
        ----------
        uri : str
            URI of artifact to fetch.
        """
        return self._client.fetch_artifact(uri)

    # Output data

    def persist_data(self,
                     data_name: Optional[Union[str, list]] = None,
                     schema_name: Optional[str] = None) -> None:
        """
        Shortcut to persist data and validation schema.

        Parameters
        ----------
        data_name : str or list, default = None
            Filename(s) for input data.
        schema_name : str, default = None
            Filename for input schema.

        """
        metadata = self.data_resource.get_metadata()

        # Data
        data = self.fetch_input_data()
        data, data_name = data_listify(data, data_name)

        for idx, path in enumerate(data):
            # try to infer source name if no name is passed
            src_name = data_name[idx] if data_name[idx] is not None \
                                      else get_name_from_uri(path)

            self.persist_artifact(data[idx], src_name, metadata)

        # Schema
        schema = self.fetch_validation_schema()
        if schema is not None:
            src_name = schema_name if schema_name is not None \
                                   else get_name_from_uri(schema)
            self.persist_artifact(schema, src_name)
        else:
            warnings.warn("No validation schema is provided!")
            return

    def persist_full_report(self,
                            report: Optional[Any] = None) -> None:
        """
        Shortcut to persist a report produced by a validation
        framework.

        Parameters
        ----------
        report : Any, default = None
            An report object produced by a validation library.

        """
        if report is None and self._report is None:
            warnings.warn("No report provided, skipping!")
            return
        if report is None:
            report = self._report
        self.persist_artifact(dict(report),
                              src_name=self._FULL_REPORT)

    def persist_inferred_schema(self,
                                schema: Optional[Any] = None) -> None:
        """
        Shortcut to persist an inferred schema produced by a validation
        framework.

        Parameters
        ----------
        schema : Any, default = None
            An inferred schema object produced by a validation library.

        """
        if schema is None and self._inf_schema is None:
            warnings.warn("No schema provided, skipping!")
            return
        if schema is None:
            schema = self._inf_schema
        self.persist_artifact(dict(schema),
                              src_name=self._SCHEMA_INFERRED)

    def persist_profile(self,
                        profile: Optional[ProfileReport] = None
                        ) -> None:
        """
        Shortcut to persist the profile made with pandas
        profiling.
        """
        if self.profile is None and profile is None:
            warnings.warn("No profile provided, skipping!")
            return
        if profile is None:
            string_html = self.profile.to_html()
        else:
            if not isinstance(profile, ProfileReport):
                raise TypeError("Invalid ProfileReport object!")
            string_html = profile.to_html()

        stringio = write_bytesio(string_html)
        self.persist_artifact(stringio, self._FULL_PROFILE)

    def persist_artifact(self,
                         src: Any,
                         src_name: Optional[str] = None,
                         metadata: Optional[dict] = None,
                         ) -> None:
        """
        Method to persist artifacts in the artifact store.

        Parameters
        ----------
        src : str, list or dict
            One or a list of URI described by a string, or a dictionary.
        src_name : str, default = None
            Filename. Required only if src is a dictionary.
        metadata: dict, default = None
            Optional metadata to attach on artifact.

        """
        if metadata is None:
            metadata = {}
        self._client.persist_artifact(src,
                                      self.run_info.run_artifacts_uri,
                                      src_name=src_name,
                                      metadata=metadata)
        self._log_artifact(src_name)

    # Frameworks wrapper methods

    @abstractmethod
    def infer_resource(self) -> Any:
        """
        Resource inference method.
        """

    @abstractmethod
    def validate_resource(self) -> Any:
        """
        Resource validation method.
        """

    # Getter

    def get_run(self) -> dict:
        """
        Return a dictionary of run info attributes.
        """
        return self.run_info.to_dict()

    @property
    def data_resource(self) -> DataResource:
        """
        Return a DataResource.
        """
        return self._data_resource

    @property
    def profile(self) -> ProfileReport:
        """
        Return ProfileReport.
        """
        return self._profile

    # Context manager

    def __enter__(self) -> Run:
        # Set run status
        self.run_info.begin_status = "active"
        self.run_info.started = get_time()
        self._log_run()
        return self

    def __exit__(self,
                 exc_type,
                 exc_value,
                 traceback) -> None:
        if exc_type is None:
            self.run_info.end_status = "finished"
        elif exc_type in (InterruptedError, KeyboardInterrupt):
            self.run_info.end_status = "interrupted"
        elif self.run_info.data_resource_uri is None:
            self.run_info.end_status = "invalid"
        else:
            self.run_info.end_status = "failed"
        self.run_info.finished = get_time()
        self._log_run()

        # Cleanup tmp files
        self._data = None
        self._val_schema = None
        clean_all(self._client.tmp_dir)

    # Dunders

    def __repr__(self) -> str:
        return str(self.run_info.to_dict())
