"""
Run module.
"""
# pylint: disable=import-error,invalid-name,too-many-instance-attributes
from __future__ import annotations

import typing
from typing import Any, Optional, Union

from datajudge.data import (BlobLog, EnvLog, DatajudgeProfile,
                            DatajudgeReport, DatajudgeSchema)
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
    infer :
        Execute schema inference over a resource.
    validate :
        Execute validation over a resource.
    profile :
        Execute profiling over a resource.
    log_schema :
        Log datajudge schema.
    log_report :
        Log datajudge report.
    log_profile :
        Log datajudge profile.
    persist_schema :
        Persist schema produced by an inference framework.
    persist_report :
        Persist report produced by a validation framework.
    persist_profile :
        Persist profile produced by a profiling framework.
    persist_artifact :
        Persist an artifact in the artifact store.
    persist_data :
        Persist input data.
    fetch_input_data :
        Fetch input data from artifact store.
    fetch_artifact :
        Fetch an artifact from artifact store.

    """

    # Constants

    _RUN_METADATA = cfg.MT_RUN_METADATA
    _RUN_ENV = cfg.MT_RUN_ENV
    _DJ_REPORT = cfg.MT_DJ_REPORT
    _DJ_SCHEMA = cfg.MT_DJ_SCHEMA
    _DJ_PROFILE = cfg.MT_DJ_PROFILE
    _ARTIFACT_METADATA = cfg.MT_ARTIFACT_METADATA

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

        # To remove
        self._val_schema = None
        self._report = None

        # Update run info
        self._get_resource()
        self._get_plugin_info()

    # Run methods

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
        if self.run_info.run_metadata_uri is None:
            return
        metadata = self._get_blob(self.run_info.to_dict())
        self._log_metadata(metadata, self._RUN_METADATA)

    def _log_env(self) -> None:
        """
        Log run's enviroment details.
        """
        if self.run_info.run_metadata_uri is None:
            return
        env_data = EnvLog().to_dict()
        metadata = self._get_blob(env_data)
        self._log_metadata(metadata, self._RUN_ENV)

    def _get_blob(self,
                  content: Optional[dict] = None) -> dict:
        """
        Return structured content to log.
        """
        if content is None:
            content = {}
        return BlobLog(self.run_info.run_id,
                       self.run_info.experiment_name,
                       self.run_info.experiment_title,
                       cfg.DATAJUDGE_VERSION,
                       self.data_resource.name,
                       self.data_resource.path,
                       content).to_dict()

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
        if self.run_info.run_metadata_uri is None:
            return
        uri = self.run_info.run_artifacts_uri
        metadata = self._get_artifact_metadata(uri, src_name)
        self._log_metadata(metadata, self._ARTIFACT_METADATA)

    def _render_obj(self,
                    plugin: Any,
                    object: Any) -> None:
        """
        Check objects to persist, render and persist them.
        """
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
        if self.run_info.run_artifacts_uri is None:
            raise AttributeError("Please configure an artifact store.")

        if metadata is None:
            metadata = {}
        self._client.persist_artifact(src,
                                      self.run_info.run_artifacts_uri,
                                      src_name=src_name,
                                      metadata=metadata)
        self._log_artifact(src_name)

    def persist_data(self,
                     data_name: Optional[Union[str, list]] = None
                    ) -> None:
        """
        Persist input data as artifact.

        Parameters
        ----------
        data_name : str or list, default = None
            Filename(s) for input data.

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

    # Inference

    def infer_wrapper(self) -> tuple:
        """
        Execute schema inference over a resource.
        Return the schema inferred by the inference framework.
        """
        self._check_plugin(self._inf_plugin)
        self.fetch_input_data()
        return self._inf_plugin.infer(self.data_resource.name,
                                      self._data)

    def infer_datajudge(self) -> dict:
        """
        Execute schema inference over a resource.
        Return the schema inferred by datajudge.
        """
        schema = self._inf_plugin.registry.get_result(
                                        self.data_resource.name)
        if schema is None:
            schema = self.infer_wrapper()

        parsed = self._inf_plugin.parse_schema(schema)
        schema = DatajudgeSchema(
                            self._inf_plugin.lib_name,
                            self._inf_plugin.lib_version,
                            self.run_info.data_resource_uri,
                            self._inf_plugin.registry.get_time(
                                        self.data_resource.name),
                            parsed)
        return schema

    def infer(self) -> tuple:
        """
        Execute schema inference over a resource.
        """
        schema = self.infer_wrapper()
        schema_dj = self.infer_datajudge()
        return schema, schema_dj

    def log_schema(self,
                   schema: DatajudgeSchema) -> None:
        """
        Log datajudge schema.

        Parameters
        ----------
        schema : dict
            A datajudge schema to be logged.

        """
        self._check_metadata_uri()
        self._check_type(schema, DatajudgeSchema)
        metadata = self._get_blob(schema.to_dict())
        self._log_metadata(metadata, self._DJ_SCHEMA)

    def persist_schema(self, schema: Any) -> None:
        """
        Persist an inferred schema produced by a validation framework.

        Parameters
        ----------
        schema : Any
            An inferred schema object produced by a validation library.

        """
        self._render_obj(self._inf_plugin, schema)

    # Validation

    def validate_wrapper(self,
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
        if self._report is None:
            self._report = self._val_plugin.validate(self._data,
                                                        constraints,
                                                        self._val_schema,
                                                        val_kwargs)
      
    def validate_datajudge(self,
                           constraints: Optional[dict] = None,
                           val_kwargs: Optional[dict] = None
                           ) -> dict:
        """
        Execute schema inference over a resource.
        Return the schema inferred by datajudge.

        Parameters
        ----------
        constraints : dict, default = None
            Constraints from configuration.
        val_kwargs : dict, default = None
            Specific framework arguments.

        """
        if self._report_dj is not None:
            return self._report_dj

        if self._report is None:
            self.validate_wrapper(constraints, val_kwargs)
        parsed = self._val_plugin.parse_report(self._report,
                                               self._val_schema)

        self._report_dj = DatajudgeReport(self._val_plugin.lib_name,
                                      self._val_plugin.lib_version,
                                      self.run_info.data_resource_uri,
                                      parsed.time,
                                      parsed.valid,
                                      parsed.errors).to_dict()

        return self._report_dj

    def validate(self,
                 constraints: Optional[dict] = None,
                 val_kwargs: Optional[dict] = None) -> tuple:
        """
        Execute validation over a resource.

        Parameters
        ----------
        constraints : dict, default = None
            Constraints from configuration.
        val_kwargs : dict, default = None
            Specific framework arguments.

        """
        report = self.validate_wrapper(constraints, val_kwargs)
        report_dj = self.validate_datajudge()
        return report, report_dj
      
    def log_report(self,
                   report: Optional[DatajudgeReport] = None
                   ) -> None:
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
        self._check_metadata_uri()
        if not isinstance(report, DatajudgeReport):
            if self._report_dj is None:
                report = self.validate_datajudge()
                if report is None:
                    warn("Unable to log report, skipping.")
                    return
            else:
                report = self._report_dj

        metadata = self._get_blob(report)
        self._log_metadata(metadata, self._DJ_REPORT)

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

    # Profiling

    def profile_wrapper(self,
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
        return self._pro_plugin.profile(self.data_resource.name,
                                        self._data,
                                        profiler_kwargs)

    def profile_datajudge(self,
                          profiler_kwargs: dict = None
                          ) -> dict:
        """
        Execute schema inference over a resource.
        Return the schema inferred by datajudge.
       
        Parameters
        ----------
        profiler_kwargs : dict, default = None
            Kwargs passed to profiler.

        """
        profile = self._pro_plugin.registry.get_result(
                                            self.data_resource.name)

        if profile is None:
            self.profile_wrapper(profiler_kwargs)

        parsed = self._pro_plugin.parse_profile(profile,
                                                self.data_resource.name)
        profile = DatajudgeProfile(self._pro_plugin.lib_name,
                                   self._pro_plugin.lib_version,
                                   self.run_info.data_resource_uri,
                                   parsed.duration,
                                   parsed.stats,
                                   parsed.fields)
        return profile

    def profile(self,
                profiler_kwargs: dict = None) -> tuple:
        """
        Execute profiling over a resource.
       
        Parameters
        ----------
        profiler_kwargs : dict, default = None
            Kwargs passed to profiler.

        """
        profile = self.profile_wrapper(profiler_kwargs)
        profile_dj = self.profile_datajudge()
        return profile, profile_dj

    def log_profile(self,
                    profile: DatajudgeProfile) -> None:
        """
        Log a data profile.

        Parameters
        ----------
        profile : Any
            A profile report to be logged.

        """
        self._check_metadata_uri()
        self._check_type(profile, DatajudgeProfile)
        metadata = self._get_blob(profile.to_dict())
        self._log_metadata(metadata, self._DJ_PROFILE)

    def persist_profile(self, profile: Any) -> None:
        """
        Persist a data profile produced by a profiling framework.

        Parameters
        ----------
        profile : Any
            A profile object produced by a profiling library.

        """
        self._render_obj(self._pro_plugin, profile)

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
        if self.run_info.run_artifacts_uri is None:
            raise AttributeError("Please configure an artifact store.")

        return self._client.fetch_artifact(uri)

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
    def _check_type(obj: Any, obj_type: Any) -> None:
        """
        Check object type.
        """
        if not isinstance(obj, obj_type):
            raise TypeError("Wrong type object passed.")

    def _check_metadata_uri(self) -> None:
        """
        Check metadata uri existence.
        """
        if self.run_info.run_metadata_uri is None:
            raise AttributeError("Please configure a metadata store.")
   
    def _check_artifact_uri(self) -> None:
        """
        Check artifact uri existence.
        """
        if self.run_info.run_artifact_uri is None:
            raise AttributeError("Please configure a artifact store.")

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
