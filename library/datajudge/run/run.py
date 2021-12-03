"""
Base class for Run objects.
"""
# pylint: disable=import-error,invalid-name
from __future__ import annotations

import json
import os
import platform
import time
import typing
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from typing import Any, List, Optional, Tuple, Union

import pandas as pd
import pandas_profiling
from pandas_profiling import ProfileReport
from psutil import virtual_memory

from datajudge.data import (ReportTuple, SchemaTuple, ShortProfile,
                            ShortReport, ShortSchema)
from datajudge.utils import config as cfg
from datajudge.utils.file_utils import clean_all
from datajudge.utils.io_utils import write_bytesio
from datajudge.utils.uri_utils import get_name_from_uri
from datajudge.utils.utils import data_listify, get_time, time_to_sec, warn

if typing.TYPE_CHECKING:
    from datajudge.client import Client
    from datajudge.data import DataResource
    from datajudge.run import RunInfo

# pylint: disable=too-many-instance-attributes


class Run:
    """
    Run object.
    The Run is the main interface to interact with data and metadata.
    It interacts both with the Client and the Data Resource/Package.

    Methods
    -------
    log_data_resource :
        Log data resource.
    log_short_report :
        Log short report.
    log_short_schema :
        Log short schema.
    log_profile :
        Log short version of pandas_profiling profile.
    persist_artifact :
        Persist an artifact in the artifact store.
    persist_data :
        Persist input data and validation schema.
    persist_full_report :
        Persist a full report produced by the validation
        framework as artifact.
    persist_inferred_schema :
        Persist an inferred schema produced by the
        validation framework as artifact.
    persist_profile :
        Persist pandas_profiling JSON and HTML profile.
    fetch_artifact :
        Fetch an artifact from data store.
    fetch_input_data :
        Fetch input data from data store.
    fetch_validation_schema :
        Fetch validation schema from data store.
    infer_profile :
        Generate a pandas_profiling profile.
    infer_schema :
        Infer schema from resource
    infer_resource :
        Do some inference on the input resource.
    validate_resource :
        Validate a resource based on validaton framework.
    get_run :
        Get run info.

    """

    __metaclass__ = ABCMeta

    _RUN_METADATA = cfg.MT_RUN_METADATA
    _DATA_RESOURCE = cfg.MT_DATA_RESOURCE
    _SHORT_REPORT = cfg.MT_SHORT_REPORT
    _SHORT_SCHEMA = cfg.MT_SHORT_SCHEMA
    _DATA_PROFILE = cfg.MT_DATA_PROFILE
    _ARTIFACT_METADATA = cfg.MT_ARTIFACT_METADATA
    _RUN_ENV = cfg.MT_RUN_ENV

    _VALID_SCHEMA = cfg.FN_VALID_SCHEMA
    _FULL_REPORT = cfg.FN_FULL_REPORT
    _SCHEMA_INFERRED = cfg.FN_INFERRED_SCHEMA
    _FULL_PROFILE_HTML = cfg.FN_FULL_PROFILE_HTML
    _FULL_PROFILE_JSON = cfg.FN_FULL_PROFILE_JSON

    def __init__(self,
                 run_info: RunInfo,
                 data_resource: DataResource,
                 client: Client,
                 overwrite: bool) -> None:

        self.data_resource = data_resource
        self._client = client
        self.run_info = run_info
        self._overwrite = overwrite

        # Local temp paths
        self._data = None
        self._val_schema = None

        # Cahcing results of inference/validation/profiling
        self.inferred = None
        self.inf_schema = None
        self._inf_schema_duration = None
        self.report = None
        self.profile = None

        self._update_library_info()
        self._update_profiler_info()
        self._log_run()

    # Run

    @abstractmethod
    def _update_library_info(self) -> None:
        """
        Update run's info about the validation framework used.
        """

    def _update_profiler_info(self) -> None:
        """
        Update run's info about the profiling framework used.
        """
        # Maybe to remove in the future? Multiple profiling libraries support?
        self.run_info.profiling_library_name = pandas_profiling.__name__
        self.run_info.profiling_library_version = pandas_profiling.__version__

    def _log_run(self) -> None:
        """
        Log run's metadata.
        """
        metadata = self._get_content(self.run_info.to_dict())
        self._log_metadata(metadata, self._RUN_METADATA)

    def _log_env(self) -> None:
        """
        Log run's enviroment details.
        """
        env_data = {
            "platform": platform.platform(),
            "pythonVersion": platform.python_version(),
            "cpuModel": platform.processor(),
            "cpuCore": os.cpu_count(),
            "ram": str(round(virtual_memory().total / (1024.0 ** 3)))+" GB"
        }
        metadata = self._get_content(env_data)
        self._log_metadata(metadata, self._RUN_ENV)

    # Data Resource

    @abstractmethod
    def _update_data_resource(self) -> None:
        """
        Update resource with inferred information.
        """

    def log_data_resource(self,
                          infer: bool = True) -> None:
        """
        Log data resource.

        Parameters
        ----------
        infer : bool, default = True
            If True, make inference on resource.

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

    # Short Report

    @abstractmethod
    def _parse_report(self,
                      nmtp: namedtuple) -> namedtuple:
        """
        Parse the report produced by the validation framework.
        """

    def _set_report(self,
                    report: Optional[Any] = None,
                    infer: bool = True) -> None:
        """
        Set private attribute 'report'.
        """
        if self.report is None:
            if report is None and infer:
                self.report = self.validate_resource()
            else:
                self.report = report

    @abstractmethod
    def _check_report(self,
                      report: Any) -> None:
        """
        Check a report before log/persist it.
        """

    def log_short_report(self,
                         report: Optional[dict] = None,
                         infer: bool = True) -> None:
        """
        Log short report.

        Parameters
        ----------
        report : Any
            A report object to be logged. If it is not
            provided, the run will check its own report attribute.
        infer : bool, default = True
            If True, try to validate the resource.

        """
        self._check_report(report)
        self._set_report(report, infer)

        if self.report is None:
            warn("No report provided! Skipped log.")
            return

        args = self._parse_report(ReportTuple)
        report_args = {
            "val_lib_name": args.val_lib_name,
            "val_lib_version": args.val_lib_version,
            "data_resource_uri": self.run_info.data_resource_uri,
            "duration": args.time,
            "valid": args.valid,
            "errors": args.errors,
        }

        short_report = ShortReport(**report_args)
        metadata = self._get_content(short_report.to_dict())
        self._log_metadata(metadata, self._SHORT_REPORT)

    # Short Schema

    @abstractmethod
    def _parse_schema(self,
                      nmtp: namedtuple) -> namedtuple:
        """
        Parse the inferred schema produced by the validation
        framework.
        """

    def _set_schema(self,
                    schema: Optional[Any] = None,
                    infer: bool = True) -> None:
        """
        Set private attribute 'inf_schema'.
        """
        if self.inf_schema is None:
            if schema is None and infer:
                start = time.perf_counter()
                self.inf_schema = self.infer_schema()
                self._inf_schema_duration = round(
                            time.perf_counter() - start, 4)
            else:
                self.inf_schema = schema

    @abstractmethod
    def _check_schema(self,
                      schema: Any) -> None:
        """
        Check a schema before log/persist it.
        """

    def log_short_schema(self,
                         schema: Optional[dict] = None,
                         infer: bool = True) -> dict:
        """
        Log short schema.

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

        if self.inf_schema is None:
            warn("No schema provided! Skipped log.")
            return

        parsed_fields, lib_name, lib_vrs = self._parse_schema(SchemaTuple)
        schema_args = {
            "val_lib_name": lib_name,
            "val_lib_version": lib_vrs,
            "data_resource_uri": self.run_info.data_resource_uri,
            "fields": parsed_fields,
            "duration": self._inf_schema_duration,
        }

        short_schema = ShortSchema(**schema_args)
        metadata = self._get_content(short_schema.to_dict())
        self._log_metadata(metadata, self._SHORT_SCHEMA)

    # Short Profile

    @staticmethod
    def _read_df(path: Union[str, List[str]],
                 file_format: str,
                 **kwargs: dict) -> pd.DataFrame:
        """
        Read a file into a pandas DataFrame.
        """

        # Check if path is a list of paths
        is_list = isinstance(path, list)

        if file_format == "csv":
            if is_list:
                list_df = [pd.read_csv(i, **kwargs) for i in path]
                df = pd.concat(list_df)
            else:
                df = pd.read_csv(path, **kwargs)
            return df

        if file_format in ["xls", "xlsx", "ods", "odf"]:
            if is_list:
                list_df = [pd.read_excel(i, **kwargs) for i in path]
                df = pd.concat(list_df)
            else:
                df = pd.read_excel(path, **kwargs)
            return df

        raise ValueError("Invalid extension.",
                         " Only CSV and XLS supported!")

    def infer_profile(self,
                      pp_kwargs: dict = None) -> ProfileReport:
        """
        Generate pandas_profiling profile.

        Parameters
        ----------
        **kwargs : dict
            Parameters for pandas_profiling.ProfileReport.

        """
        file_format, pandas_kwargs = self._parse_inference()
        df = self._read_df(self.fetch_input_data(),
                           file_format,
                           **pandas_kwargs)
        profile = ProfileReport(df, **pp_kwargs)
        return profile

    def _parse_profile(self) -> dict:
        """
        Parse the profile generated by pandas profiling.
        """

        # Profile preparation
        json_str = self.profile.to_json()
        json_str = json_str.replace("NaN", "null")
        full_profile = json.loads(json_str)

        # Short profile args
        args = {
            k: full_profile.get(k, {}) for k in cfg.PROFILE_COLUMNS
        }

        # Variables overwriting by filtering
        var = args.get("variables")
        for key in var:
            args["variables"][key] = {
                k: var[key][k] for k in cfg.PROFILE_FIELDS
            }

        # "Rename" variables with fields and tables with stats
        args["fields"] = args.pop("variables")
        args["stats"] = args.pop("table")

        # Extract duration from analysis and set as key
        # and pop analysis
        duration = args.get("analysis", {}).get("duration")
        args["duration"] = time_to_sec(duration)
        args.pop("analysis")

        return args

    def _set_profile(self,
                     profile: Optional[ProfileReport] = None,
                     infer: bool = True,
                     pp_kwargs: dict = None) -> None:
        """
        Set private attribute 'profile'.
        """
        if self.profile is None:
            if profile is None and infer:
                self.profile = self.infer_profile(pp_kwargs)
            else:
                self.profile = profile

    @staticmethod
    def _check_profile(profile: Optional[ProfileReport] = None
                       ) -> None:
        """
        Check validity of profile.
        """
        if profile is not None and not isinstance(profile, ProfileReport):
            raise TypeError("Expected pandas_profiling Profile!")

    def log_profile(self,
                    profile: Optional[ProfileReport] = None,
                    infer: bool = True,
                    pp_kwargs: dict = None
                    ) -> None:
        """
        Log a pandas_profiling profile.

        Parameters
        ----------
        profile : ProfileReport, default = None
            A pandas_profiling report to be logged. If it is not
            provided, the run will check its own profile attribute.
        infer : bool, default = True
            If True, profile the resource.
        pp_kwargs : dict, default = None
            Kwargs passed to ProfileReport.

        """
        self._check_profile(profile)
        self._set_profile(profile, infer, pp_kwargs)

        if self.profile is None:
            warn("No profile provided! Skipped log.")
            return

        parsed = self._parse_profile()
        parsed["data_resource_uri"] = self.run_info.data_resource_uri
        parsed["pro_lib_name"] = pandas_profiling.__name__
        parsed["pro_lib_version"] = pandas_profiling.__version__
        short_profile = ShortProfile(**parsed)
        metadata = self._get_content(short_profile.to_dict())
        self._log_metadata(metadata, self._DATA_PROFILE)

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
        Log artifact metadata.
        """
        uri = self.run_info.run_artifacts_uri
        metadata = self._get_artifact_metadata(uri, src_name)
        self._log_metadata(metadata, self._ARTIFACT_METADATA)

    # Metadata

    def _get_content(self,
                     content: Optional[dict] = None) -> dict:
        """
        Return structured content to log.
        """
        metadata = {
            "runId": self.run_info.run_id,
            "experimentId": self.run_info.experiment_id,
            "experimentName": self.run_info.experiment_name,
            "datajudgeVersion": cfg.DATAJUDGE_VERSION,
            "contents": content
        }
        return metadata

    def _log_metadata(self,
                      metadata: dict,
                      src_type: str) -> None:
        """
        Log generic metadata.
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
        Fetch artifact from backend.

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
        Persist data and validation schema.

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
            return
        warn("No validation schema is provided!")

    def persist_full_report(self,
                            report: Optional[Any] = None) -> None:
        """
        Persist a report produced by a validation framework.

        Parameters
        ----------
        report : Any, default = None
            An report object produced by a validation library.

        """
        if report is None and self.report is None:
            warn("No report provided, skipping!")
            return
        if report is None:
            report = self.report
        self.persist_artifact(dict(report),
                              src_name=self._FULL_REPORT)

    def persist_inferred_schema(self,
                                schema: Optional[Any] = None) -> None:
        """
        Persist an inferred schema produced by a validation framework.

        Parameters
        ----------
        schema : Any, default = None
            An inferred schema object produced by a validation library.

        """
        if schema is None and self.inf_schema is None:
            warn("No schema provided, skipping!")
            return
        if schema is None:
            schema = self.inf_schema
        self.persist_artifact(dict(schema),
                              src_name=self._SCHEMA_INFERRED)

    def persist_profile(self,
                        profile: Optional[ProfileReport] = None
                        ) -> None:
        """
        Persist the profile made with pandas_profiling,
        both in JSON and HTML format.
        """
        if self.profile is None and profile is None:
            warn("No profile provided, skipping!")
            return
        if profile is None:
            string_html = self.profile.to_html()
            string_json = self.profile.to_json()
        else:
            if not isinstance(profile, ProfileReport):
                raise TypeError("Invalid ProfileReport object!")
            string_html = profile.to_html()
            string_json = profile.to_json()

        string_json = string_json.replace("NaN", "null")

        strio_html = write_bytesio(string_html)
        strio_json = write_bytesio(string_json)
        self.persist_artifact(strio_html, self._FULL_PROFILE_HTML)
        self.persist_artifact(strio_json, self._FULL_PROFILE_JSON)

    def persist_artifact(self,
                         src: Any,
                         src_name: Optional[str] = None,
                         metadata: Optional[dict] = None,
                         ) -> None:
        """
        Persist artifacts in the artifact store.

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
    def infer_schema(self) -> Any:
        """
        Parse the inferred schema produced by the validation
        framework.
        """

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

    @abstractmethod
    def _parse_inference(self) -> Tuple[str, dict]:
        """
        Parse inference from specific validation framework.
        Used by profiling.
        """

    # Context manager

    def __enter__(self) -> Run:
        # Set run status
        self.run_info.begin_status = "active"
        self.run_info.started = get_time()
        self._log_run()
        self._log_env()
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
        try:
            clean_all(self._client.tmp_dir)
        except FileNotFoundError:
            pass

    # Dunders

    def __repr__(self) -> str:
        return str(self.run_info.to_dict())
