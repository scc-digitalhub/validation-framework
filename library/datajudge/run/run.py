"""
Run module.
"""
# pylint: disable=import-error,invalid-name,too-many-instance-attributes
from __future__ import annotations

import typing
from typing import Any, Optional, Union

from datajudge.data import (BlobLog, EnvLog, ShortProfile,
                            ShortReport, ShortSchema)
from datajudge.run.plugin_factory import get_plugin
from datajudge.utils import config as cfg
from datajudge.utils.file_utils import clean_all
from datajudge.utils.uri_utils import get_name_from_uri
from datajudge.utils.utils import data_listify, get_time, warn

if typing.TYPE_CHECKING:
    from datajudge.client import Client
    from datajudge.data import DataResource
    from datajudge.run import RunInfo


class Run:
    """
    Run object.
    The Run is the main interface to interact with data, metadata and
    operational framework. With the Run, you can infer, validate and profile
    resources, log and persist data and metadata.
    It interacts both with the Client and the Data Resource/Package.

    Methods
    -------
    infer_resource :
        Execute inference over a resource.
    infer_schema :
        Execute schema inference over a resource.
    infer :
        Execute inference both on schema and resource.
    validate :
        Execute validation over a resource.
    profile :
        Execute profiling over a resource.
    log_data_resource :
        Log data resource.
    log_short_schema :
        Log short schema.
    log_short_report :
        Log short report.
    log_profile :
        Log short profile.
    persist_artifact :
        Persist an artifact in the artifact store.
    persist_data :
        Persist input data (and optionally a validation schema).
    persist_report :
        Persist a report produced by a validation framework.
    persist_schema :
        Persist an inferred schema produced by an inference framework.
    persist_profile :
        Persist a profile produced by a profiling framework.
    fetch_artifact :
        Fetch an artifact from artifact store.
    fetch_input_data :
        Fetch input data from artifact store.
    fetch_validation_schema : 
        Fetch a validation schema from artifact store.
    
    """

    # Constants

    _RUN_METADATA = cfg.MT_RUN_METADATA
    _RUN_ENV = cfg.MT_RUN_ENV
    _DATA_RESOURCE = cfg.MT_DATA_RESOURCE
    _SHORT_REPORT = cfg.MT_SHORT_REPORT
    _SHORT_SCHEMA = cfg.MT_SHORT_SCHEMA
    _DATA_PROFILE = cfg.MT_DATA_PROFILE
    _ARTIFACT_METADATA = cfg.MT_ARTIFACT_METADATA
    _DJ_VERSION = cfg.DATAJUDGE_VERSION

    # Constructor

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
        # It's cached only the result of the framework used,
        # not the shorter version provided by datajudge
        self._schema = None
        self._report = None
        self._profile = None

        # Constant to measure duration of schema inference task
        self._time_inf_sch = None

    # Run metadata

    def _get_resource(self) -> None:
        """
        Insert packages/resources into Run Info.
        """
        self.run_info.data_resource = self.data_resource.to_dict()

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
                "libVersion": plugin.lib_version
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

    def infer_resource(self) -> dict:
        """
        Execute inference over a resource.
        """
        self._check_plugin(self._inf_plugin)
        self.fetch_input_data()
        self._inf_plugin.update_data_resource(
                                self.data_resource,
                                self._data)
        return self.data_resource.to_dict()

    def log_data_resource(self) -> None:
        """
        Log data resource.
        """
        metadata = self._get_blob(self.data_resource.to_dict())
        self._log_metadata(metadata, self._DATA_RESOURCE)

        # Update run info
        if self.run_info.data_resource_uri is None:
            uri_resource = self._client.get_data_resource_uri(
                                            self.run_info.experiment_name,
                                            self.run_info.run_id)
            self.run_info.data_resource_uri = uri_resource

    # Short schema

    def infer_schema(self) -> Any:
        """
        Execute schema inference over a resource.
        """
        self._check_plugin(self._inf_plugin)
        self.fetch_input_data()
        self.fetch_validation_schema()

        # Cache schema on run.
        if self._schema is None:
            self._schema, self._time_inf_sch = \
                        self._inf_plugin.infer_schema(self._data)
        return self._schema

    def log_short_schema(self,
                         schema: Optional[dict] = None
                         ) -> None:
        """
        Log short schema. The method register a schema object
        on the run derived from a specific inference library.

        Parameters
        ----------
        schema : dict, default = None
            An inferred schema to be logged. If it is not
            provided, the run will check its own schema attribute.

        """
        schema = self._check_obj(schema, self._schema)
        self._inf_plugin.validate_schema(schema)
        parsed = self._inf_plugin.parse_schema(schema,
                                               self._val_schema)
        short_schema = ShortSchema(
                            self._inf_plugin.lib_name,
                            self._inf_plugin.lib_version,
                            self.run_info.data_resource_uri,
                            self._time_inf_sch,
                            parsed).to_dict()
        metadata = self._get_blob(short_schema)
        self._log_metadata(metadata, self._SHORT_SCHEMA)

    def infer(self) -> tuple:
        """
        Execute inference and schema inference over a resource.
        """
        return self.infer_resource(), self.infer_schema()

    # Short report

    def validate(self,
                 constraints: Optional[dict] = None,
                 val_kwargs: Optional[dict] = None) -> Any:
        """
        Execute validation of a resource.

        Parameters
        ----------
        constraints : dict, default = None
            Constraints from configuration.
        val_kwargs : dict, default = None
            Specific framework arguments.

        """
        self._check_plugin(self._val_plugin)
        self.fetch_input_data()
        self.fetch_validation_schema()

        # Cache report on run.
        if self._report is None:
            self._report = self._val_plugin.validate(self._data,
                                                     constraints,
                                                     self._val_schema,
                                                     val_kwargs)
        return self._report

    def log_short_report(self,
                         report: Optional[Any] = None) -> None:
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
        report = self._check_obj(report, self._report)
        self._val_plugin.validate_report(report)
        parsed = self._val_plugin.parse_report(report,
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

    def profile(self,
                profiler_kwargs: dict = None) -> Any:
        """
        Execute profiling on a resource.

        Parameters
        ----------
        profiler_kwargs : dict, default = None
            Kwargs passed to profiler.

        """
        self._check_plugin(self._pro_plugin)
        self.fetch_input_data()

        # Cache profile on run.
        if self._profile is None:
            self._profile = self._pro_plugin.profile(self._data,
                                                     self.data_resource,
                                                     profiler_kwargs)
        return self._profile

    def log_profile(self,
                    profile: Optional[Any] = None) -> None:
        """
        Log a data profile.

        Parameters
        ----------
        profile : Any, default = None
            A profile report to be logged. If it is not provided,
            the run will check its own profile attribute.

        """
        profile = self._check_obj(profile, self._profile)
        self._pro_plugin.validate_profile(profile)
    
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
        metadata = {
            "uri": uri,
            "name": name
        }
        return self._get_blob(metadata)

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
            return
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

    def persist_report(self,
                       report: Optional[Any] = None) -> None:
        """
        Persist a report produced by a validation framework.

        Parameters
        ----------
        report : Any, default = None
            An report object produced by a validation library.

        """
        self._render_obj(self._val_plugin,
                             self._report,
                             report)

    def persist_schema(self,
                       schema: Optional[Any] = None) -> None:
        """
        Persist an inferred schema produced by a validation framework.

        Parameters
        ----------
        schema : Any, default = None
            An inferred schema object produced by a validation library.

        """
        self._render_obj(self._inf_plugin,
                             self._schema,
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
        self._render_obj(self._pro_plugin,
                             self._profile,
                             profile)
            
    def _render_obj(self,
                    plugin: Any,
                    cached: Any,
                    object: Optional[Any] = None) -> None:
        """
        Check objects to persist, render and persist them.
        """
        object = self._check_obj(object, cached)
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

    # Utils
    
    @staticmethod
    def _check_plugin(plugin: Any) -> None:
        """
        Check plugin existence
        """
        if plugin is None:
            raise RuntimeError("Please configure the plugin " +
                               "in the run configuration.")

    @staticmethod
    def _check_obj(obj: Any,
                   attribute: Any) -> None:
        """
        Check object existence or fetch from run cache.
        """
        if obj is None:
            if attribute is None:
                raise RuntimeError("No object provided.")
            return attribute
        return obj

    # Context manager

    def __enter__(self) -> Run:
        # Update run info
        self._get_resource()
        self._get_plugin_info()
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
