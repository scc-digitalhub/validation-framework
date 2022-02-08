"""
Base class for Run objects. It includes a method to build
the plugins to executes various operations.
"""
# pylint: disable=import-error,invalid-name
from __future__ import annotations

import typing
from typing import Any, Optional, Union

from datajudge.data import BlobLog, EnvLog
from datajudge.data import ShortSchema, ShortProfile, ShortReport
from datajudge.run.plugin_factory import get_plugin
from datajudge.utils import config as cfg
from datajudge.utils.file_utils import clean_all
from datajudge.utils.uri_utils import get_name_from_uri
from datajudge.utils.utils import data_listify, get_time, warn

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
    log_short_report :
        Log short report.
    log_profile :
        Log short version of pandas_profiling profile.
    log_data_resource :
        Log data resource.
    log_short_schema :
        Log short schema.
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
    infer_profile :
        Generate a pandas_profiling profile.
    validate_resource :
        Validate a resource based on validaton framework.
    get_run :
        Get run info.

    """

    _RUN_METADATA = cfg.MT_RUN_METADATA
    _DATA_RESOURCE = cfg.MT_DATA_RESOURCE
    _SHORT_REPORT = cfg.MT_SHORT_REPORT
    _SHORT_SCHEMA = cfg.MT_SHORT_SCHEMA
    _DATA_PROFILE = cfg.MT_DATA_PROFILE
    _ARTIFACT_METADATA = cfg.MT_ARTIFACT_METADATA

    _RUN_ENV = cfg.MT_RUN_ENV
    _DJ_VERSION = cfg.DATAJUDGE_VERSION

    def __init__(self,
                 run_info: RunInfo,
                 data_resource: DataResource,
                 client: Client,
                 overwrite: bool) -> None:

        self.data_resource = data_resource
        self._client = client
        self.run_info = run_info
        self._overwrite = overwrite

        # Plugin
        self._inf_plugin = get_plugin(
            self.run_info.run_config.inference)
        self._val_plugin = get_plugin(
            self.run_info.run_config.validation)
        self._pro_plugin = get_plugin(
            self.run_info.run_config.profiling)
        self._sna_plugin = get_plugin(
            self.run_info.run_config.snapshot)

        # Local temp paths
        self._data = None
        self._val_schema = None

        # Cahcing results of inference/validation/profiling
        self._resource_inferred = None
        self._schema_inferred = None
        self._report_validation = None
        self._profile = None

        # Constant to measure duration of schema inference task
        self._inf_schema_duration = None

        # Preliminary log
        self._get_plugin_info()
        self._log_run()
        self._log_env()

    # Run

    def _get_plugin_info(self) -> None:
        """
        Get plugins used libs.
        """
        self.run_info.run_libraries =  {
            "validation": self._get_plugin_lib(self._val_plugin),
            "inference": self._get_plugin_lib(self._inf_plugin),
            "profiling": self._get_plugin_lib(self._pro_plugin),
            "snapshot": self._get_plugin_lib(self._sna_plugin)
        }
    
    @staticmethod
    def _get_plugin_lib(plugin) -> Optional[dict]:
        """
        Return library name/version of a plugin.
        """
        if plugin is not None:
            return {
                "libName": plugin.lib_name,
                "libVerision": plugin.lib_version
            }

    def _log_run(self) -> None:
        """
        Log run's metadata.
        """
        metadata = self._get_blob(self.run_info.to_dict())
        self._log_metadata(metadata, self._RUN_METADATA)

    def _log_env(self) -> None:
        """
        Log run's enviroment details.
        """
        env_data = EnvLog().to_dict()
        metadata = self._get_blob(env_data)
        self._log_metadata(metadata, self._RUN_ENV)

    # Data Resource

    def _update_data_resource(self) -> None:
        """
        Update resource with inferred information.
        """
        self._inf_plugin.update_data_resource(
                                self.data_resource,
                                self._data)

    def log_data_resource(self,
                          infer: bool = True) -> None:
        """
        Log data resource.

        Parameters
        ----------
        infer : bool, default = True
            If True, make inference on a resource, otherwise
            log it as it is.

        """
        if self._inf_plugin is None:
            warn("Inferencer disabled! Skipped log.")
            return

        self.fetch_input_data()

        if infer:
            self._update_data_resource()

        metadata = self._get_blob(self.data_resource.to_dict())
        self._log_metadata(metadata, self._DATA_RESOURCE)

        # Update run info
        if self.run_info.data_resource_uri is None:
            uri_resource = self._client.get_data_resource_uri(
                                                self.run_info.run_id)
            self.run_info.data_resource_uri = uri_resource

    # Short schema

    def _set_schema(self,
                    schema: Optional[Any] = None,
                    infer: bool = True) -> None:
        """
        Set private attribute 'inf_schema'.
        """
        if self._schema_inferred is None:
            if schema is None and infer:
                self._schema_inferred, self._inf_schema_duration = \
                                self._inf_plugin.infer_schema(self._data)
            else:
                self._schema_inferred = schema

    def log_short_schema(self,
                         schema: Optional[dict] = None
                         ) -> dict:
        """
        Log short schema. The method register a schema object
        on the run derived from a specific inference library.

        Parameters
        ----------
        schema : dict, default = None
            An inferred schema to be logged. If it is not
            provided, the run will check its own schema attribute.

        """
        if self._inf_plugin is None:
            warn("Inferencer disabled! Skipped log.")
            return

        self.fetch_input_data()
        self.fetch_validation_schema()

        self._inf_plugin.validate_schema(schema)
        self._set_schema(schema)

        if self._schema_inferred is None:
            warn("No schema provided! Skipped log.")
            return

        parsed = self._inf_plugin.parse_schema(self._schema_inferred,
                                               self._val_schema)

        short_schema = ShortSchema(
                            self._inf_plugin.lib_name,
                            self._inf_plugin.lib_version,
                            self.run_info.data_resource_uri,
                            self._inf_schema_duration,
                            parsed).to_dict()
        metadata = self._get_blob(short_schema)
        self._log_metadata(metadata, self._SHORT_SCHEMA)

    # Short report

    def _set_report(self,
                    report: Optional[Any] = None,
                    kwargs: Optional[dict] = None) -> None:
        """
        Set private attribute 'report'.
        """
        if self._report_validation is None:
            if report is None:
                self._report_validation = self._val_plugin.validate(
                                                            self._data,
                                                            self._val_schema,
                                                            kwargs)
            else:
                self._report_validation = report

    def log_short_report(self,
                         report: Optional[dict] = None,
                         kwargs: Optional[dict] = None) -> None:
        """
        Log short report.

        Parameters
        ----------
        report : Any
            A report object to be logged. If it is not
            provided, the run will check its own report attribute.
        kwargs : dict, default = None
            Validation arguments.

        """
        if self._val_plugin is None:
            warn("Validator disabled! Skipped log.")
            return

        self.fetch_input_data()
        self.fetch_validation_schema()

        self._val_plugin.validate_report(report)
        self._set_report(report, kwargs)

        if self._report_validation is None:
            warn("No report provided! Skipped log.")
            return

        parsed = self._val_plugin.parse_report(self._report_validation,
                                               self._val_schema)

        blob = ShortReport(self._val_plugin.lib_name,
                           self._val_plugin.lib_version,
                           self.run_info.data_resource_uri,
                           parsed.time,
                           parsed.valid,
                           parsed.errors).to_dict()

        metadata = self._get_blob(blob)
        self._log_metadata(metadata, self._SHORT_REPORT)

    # Short profile
    def _set_profile(self,
                     profile: Optional[Any] = None,
                     infer: bool = True,
                     profiler_kwargs: dict = None) -> None:
        """
        Set private attribute 'profile'.
        """
        if self._profile is None:
            if profile is None and infer:
                self._profile = self._pro_plugin.profile(self._data,
                                                         self.data_resource,
                                                         profiler_kwargs)
            else:
                self._profile = profile

    def log_profile(self,
                    profile: Optional[Any] = None,
                    infer: bool = True,
                    profiler_kwargs: dict = None
                    ) -> None:
        """
        Log a data profile.

        Parameters
        ----------
        profile : Any, default = None
            A profile report to be logged. If it is not provided,
            the run will check its own profile attribute.
        infer : bool, default = True
            If True, profile the resource.
        profiler_kwargs : dict, default = None
            Kwargs passed to profiler.

        """
        self.fetch_input_data()

        if self._pro_plugin is None:
            warn("Profiler disabled! Skipped log.")
            return

        self._pro_plugin.validate_profile(profile)
        self._set_profile(profile, infer, profiler_kwargs)

        if self._profile is None:
            warn("No profile provided! Skipped log.")
            return

        parsed = self._pro_plugin.parse_profile(self._profile)

        blob = ShortProfile(self._pro_plugin.lib_name,
                            self._pro_plugin.lib_version,
                            self.run_info.data_resource_uri,
                            parsed.duration,
                            parsed.stats,
                            parsed.fields).to_dict()

        metadata = self._get_blob(blob)
        self._log_metadata(metadata, self._DATA_PROFILE)

    # Artifact metadata

    def _get_artifact_metadata(self,
                               uri: str,
                               name: str) -> dict:
        """
        Build artifact metadata.
        """
        metadata = self._get_blob()
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

    def _get_blob(self,
                  content: Optional[dict] = None) -> dict:
        """
        Return structured content to log.
        """
        if content is None:
            content = {}
        metadata = BlobLog(self.run_info.run_id,
                           self.run_info.experiment_name,
                           self.run_info.experiment_title,
                           self._DJ_VERSION,
                           content).to_dict()
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

    def fetch_validation_schema(self) -> str:
        """
        Fetch validation schema from backend and return temp file path.
        """
        if self.data_resource.schema is None:
            return None
        if self._val_schema is None:
            self._val_schema = self.fetch_artifact(self.data_resource.schema)
        return self._val_schema

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
                     validation_schema: bool = False,
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
        if validation_schema:
            schema = self.fetch_validation_schema()
            if schema is not None:
                src_name = schema_name if schema_name is not None \
                                    else get_name_from_uri(schema)
                self.persist_artifact(schema, src_name)
                return
            warn("No validation schema is provided!")

    def persist_full_report(self,
                            report: Optional[Any] = None
                            ) -> None:
        """
        Persist a report produced by a validation framework.

        Parameters
        ----------
        report : Any, default = None
            An report object produced by a validation library.

        """
        self._persist_object(self._val_plugin,
                             self._report_validation,
                             report)

    def persist_inferred_schema(self,
                                schema: Optional[Any] = None
                                ) -> None:
        """
        Persist an inferred schema produced by a validation framework.

        Parameters
        ----------
        schema : Any, default = None
            An inferred schema object produced by a validation library.

        """
        self._persist_object(self._inf_plugin,
                             self._schema_inferred,
                             schema)

    def persist_profile(self,
                        profile: Optional[Any] = None
                        ) -> None:
        """
        Persist a data profile produced by a profiling framework.

        Parameters
        ----------
        profile : Any, default = None
            A profile object produced by a profiling library.

        """
        self._persist_object(self._pro_plugin,
                             self._profile,
                             profile)
            
    def _persist_object(self,
                        plugin: Any,
                        cached: Any,
                        object: Optional[Any] = None
                        ) -> None:
        
        if object is None:
            if cached is None:
                warn("No object provided, skipping!")
                return
            object = cached

        rendered = plugin.render_object(object)
        for obj in rendered:
            self.persist_artifact(obj.object, 
                                  obj.filename)

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
        elif exc_type in (AttributeError, ):
            self.run_info.end_status = "failed"
        elif self.run_info.data_resource_uri is None:
            self.run_info.end_status = "invalid"
        else:
            self.run_info.end_status = "failed"
        self.run_info.finished = get_time()
        self._log_run()

        # Cleanup tmp files
        try:
            clean_all(self._client.tmp_dir)
        except FileNotFoundError:
            pass

    # Dunders

    def __repr__(self) -> str:
        return str(self.run_info.to_dict())
