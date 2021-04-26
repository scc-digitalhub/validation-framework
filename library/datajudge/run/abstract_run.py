"""
AbstractRun module.
Implementations of a Run abstract class.
"""
from __future__ import annotations

import json
import typing
from abc import ABCMeta, abstractmethod
from copy import deepcopy
from io import BytesIO
from typing import Any, Dict, List, Optional, Union

from datajudge.data import ShortReport, ShortSchema
from datajudge.utils.constants import FileNames, MetadataType
from datajudge.utils.time_utils import get_time
from datajudge.utils.uri_utils import get_name_from_uri, test_uri_access
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
    _RUN_METADATA = MetadataType.RUN_METADATA.value
    _DATA_RESOURCE = MetadataType.DATA_RESOURCE.value
    _SHORT_REPORT = MetadataType.SHORT_REPORT.value
    _SHORT_SCHEMA = MetadataType.SHORT_SCHEMA.value
    _DATA_PROFILE = MetadataType.DATA_PROFILE.value
    _ARTIFACT_METADATA = MetadataType.ARTIFACT_METADATA.value

    _VALID_SCHEMA = FileNames.VALID_SCHEMA.value
    _FULL_REPORT = FileNames.FULL_REPORT.value
    _SCHEMA_INFERRED = FileNames.SCHEMA_INFERRED.value
    _FULL_PROFILE = FileNames.FULL_PROFILE.value

    def __init__(self,
                 run_info: RunInfo,
                 data_resource: DataResource,
                 client: Client,
                 overwrite: bool) -> None:

        self._data_resource = data_resource
        self._client = client
        self.run_info = run_info
        self._overwrite = overwrite
        self._direct_access_data = False

        self._data = None
        self._val_schema = None

        self._inferred = None
        self._inf_schema = None
        self._report = None

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

    def _create_short_report(self,
                             kwargs: dict) -> ShortReport:
        """
        Return a ShortReport object.
        """
        return ShortReport(self.run_info.data_resource_uri,
                           self.run_info.experiment_name,
                           self.run_info.run_id,
                           **kwargs)

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
            parsed = self._parse_report(self._report, report_args)
            short_schema = self._create_short_report(parsed)
        else:
            short_schema = self._create_short_report(report_args)

        metadata = self._get_content(short_schema.to_dict())

        self._log_metadata(metadata, self._SHORT_REPORT)

    # Short schema

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

    @abstractmethod
    def _infer_schema(self) -> Any:
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

    def _parse_profile(self,
                       profile: Any) -> Any:
        """
        Parse the profile generated by pandas profiling.
        """

    def log_profile(self,
                    profile: Any) -> None:
        """
        Method to log a pandas profile.
        """

    # Artifact metadata

    def _get_artifact_metadata(self,
                               name: str,
                               uri: str) -> dict:
        metadata = self._get_content()
        metadata.pop("contents")
        metadata["name"] = name
        metadata["uri"] = uri
        return metadata

    def _log_artifact(self,
                      src: Any,
                      src_name: Optional[str] = None
                      ) -> None:
        """
        Method to log artifacts metadata.
        """
        uri = self.run_info.run_artifacts_uri
        names = []
        if isinstance(src, list):
            names.extend(src)
        elif isinstance(src, str):
            names.append(src)
        else:
            names.append(src_name)

        for name in names:
            metadata = self._get_artifact_metadata(name, uri)
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

    def fetch_validation_schema(self,
                                no_cached: bool = False) -> dict:
        """
        Fetch validation schema from backend.

        Parameters
        ----------
        no_cached : bool, default = False
            If True, return validation schema without store it
            on run.

        Returns
        -------
        dict

        """
        if self._val_schema is not None:
            return deepcopy(self._val_schema)

        obj = self.fetch_artifact(self.data_resource.schema)
        schema = json.load(obj)

        if no_cached:
            return schema

        self._val_schema = schema
        return deepcopy(self._val_schema)

    def fetch_input_data(self,
                         no_cached: bool = False) -> BytesIO:
        """
        Fetch data from backend.

        Parameters
        ----------
        no_cached : bool, default = False
            If True, return data without store them
            on run.

        Returns
        -------
        BytesIO

        """
        if self._data is not None:
            return deepcopy(self._data)

        if isinstance(self.data_resource.path, list):
            obj = [self.fetch_artifact(i) for i in self.data_resource.path]
        else:
            obj = self.fetch_artifact(self.data_resource.path)

        if no_cached:
            return obj

        self._data = obj
        return deepcopy(self._data)

    def fetch_artifact(self,
                       uri: str) -> BytesIO:
        """
        Method to fetch artifact from backend.

        Parameters
        ----------
        uri : str
            URI of artifact to fetch.

        Returns
        -------
        BytesIO

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
        # Data
        data = self.fetch_input_data(no_cached=True)
        data, data_name = data_listify(data, data_name)
        path_list, _ = data_listify(self.data_resource.path, None)

        for idx, path_name in enumerate(path_list):
            # try to infer source name if no name is passed
            src_name = data_name[idx] if data_name[idx] is not None \
                                      else get_name_from_uri(path_name)

            self.persist_artifact(data[idx], src_name)

        # Schema
        schema = self.fetch_validation_schema(no_cached=True)
        schema_path = self.data_resource.schema
        if schema_path is not None:
            src_name = schema_name if schema_name is not None \
                                   else get_name_from_uri(schema_path)
            self.persist_artifact(schema, src_name)

    def persist_full_report(self,
                            report: dict) -> None:
        """
        Shortcut to persist the full report produced
        by a validation framework.

        Parameters
        ----------
        report : Any
            A generic report object, specific for the library.

        """
        self._check_report(report)
        self.persist_artifact(
                    dict(report),
                    src_name=self._FULL_REPORT)

    def persist_inferred_schema(self,
                                schema: Optional[Any] = None) -> None:
        """
        Shortcut to persist the full report produced
        by a validation framework.

        Parameters
        ----------
        report : Any, default = None
            A generic schema object, specific for the library.

        """
        if schema is None and self._inf_schema is None:
            return
        # Maybe to rewrite the check
        self._check_schema(schema)
        self.persist_artifact(dict(self._inf_schema),
                              src_name=self._SCHEMA_INFERRED)

    def persist_profile(self,
                        profile: Any) -> None:
        """
        Shortcut to persist the profile made with pandas
        profiling.
        """

    def persist_artifact(self,
                         src: Any,
                         src_name: Optional[str] = None
                         ) -> None:
        """
        Method to persist artifacts in the artifact store.

        Parameters
        ----------
        src : str, list or dict
            One or a list of URI described by a string, or a dictionary.
        src_name : str, default = None
            Filename. Required only if src is a dictionary.

        """
        self._client.persist_artifact(src,
                                      self.run_info.run_artifacts_uri,
                                      src_name=src_name)
        self._log_artifact(src, src_name)

    # Framework wrapper methods

    @abstractmethod
    def _infer_resource(self) -> Any:
        """
        Resource inference method.
        """

    @abstractmethod
    def validate_resource(self) -> Any:
        """
        Resource validation method.
        """

    # Other
    def _test_data_access(self) -> None:
        """
        Test access to data.
        """
        uri = self.data_resource.path
        if isinstance(uri, list):
            uri = uri[0]
        self._direct_access_data = test_uri_access(uri)

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
    def report(self) -> Any:
        """
        Return a report.
        """
        return self._report

    @property
    def inf_schema(self) -> Any:
        """
        Return inferred schema.
        """
        return self._inf_schema

    # Context manager

    def __enter__(self) -> Run:
        # Set run status
        self._test_data_access()
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

    # Dunders

    def __repr__(self) -> str:
        return str(self.run_info.to_dict())
