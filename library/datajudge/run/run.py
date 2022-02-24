"""
Run module.
"""
# pylint: disable=import-error,invalid-name,too-many-instance-attributes
from __future__ import annotations

import typing
from typing import Any, Optional, Union

from datajudge.data import BlobLog, EnvLog
from datajudge.utils import config as cfg
from datajudge.utils.file_utils import clean_all
from datajudge.utils.uri_utils import get_name_from_uri
from datajudge.utils.utils import data_listify, get_time

if typing.TYPE_CHECKING:
    from datajudge.client import Client
    from datajudge.run import RunInfo, PluginHandler


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

    # Constants to describe metadata types

    _RUN_METADATA = cfg.MT_RUN_METADATA
    _RUN_ENV = cfg.MT_RUN_ENV
    _DJ_REPORT = cfg.MT_DJ_REPORT
    _DJ_SCHEMA = cfg.MT_DJ_SCHEMA
    _DJ_PROFILE = cfg.MT_DJ_PROFILE
    _ARTIFACT_METADATA = cfg.MT_ARTIFACT_METADATA

    # Constructor

    def __init__(self,
                 run_info: RunInfo,
                 plugin_handler: PluginHandler,
                 client: Client,
                 overwrite: bool) -> None:

        self.run_info = run_info
        self._client = client
        self.plugin_handler = plugin_handler
        self._overwrite = overwrite

        # Local temp paths
        self._data = None

        # To remove
        self._val_schema = None

    # Run methods

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
                       self.run_info.data_resource.get("name"),
                       self.run_info.data_resource.get("path"),
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

        # To do, basic inference metadata?
        metadata = {}

        # Data
        data = self.fetch_input_data()
        data, data_name = data_listify(data, data_name)
        for idx, path in enumerate(data):
            # try to infer source name if no name is passed
            src_name = data_name[idx] if data_name[idx] is not None \
                                      else get_name_from_uri(path)
            self.persist_artifact(data[idx], src_name, metadata)

    # Inference

    def infer_wrapper(self,
                      inference_kwargs: Optional[dict] = None) -> Any:
        """
        Execute schema inference over a resource.

        Parameters
        ----------
        inference_kwargs : dict, default = None
            Mappers for specific framework arguments.

        """
        self.fetch_input_data()
        return self.plugin_handler.infer(self.run_info.data_resource.get("name"),
                                         self._data,
                                         inference_kwargs)

    def infer_datajudge(self,
                        inference_kwargs: Optional[dict] = None) -> dict:
        """
        Produce datajudge inference schema.
        
        Parameters
        ----------
        inference_kwargs : dict, default = None
            Mappers for specific framework arguments.

        """
        schema = self.infer_wrapper(inference_kwargs)
        return self.plugin_handler.produce_schema(schema)

    def infer(self,
              inference_kwargs: Optional[dict] = None) -> tuple:
        """
        Execute schema inference over a resource.
        
        Parameters
        ----------
        inference_kwargs : dict, default = None
            Mappers for specific framework arguments.

        """
        schema = self.infer_wrapper()
        schema_dj = self.infer_datajudge()
        return schema, schema_dj

    def log_schema(self, schema: dict) -> None:
        """
        Log datajudge schema.

        Parameters
        ----------
        schema : dict
            A datajudge schema to be logged.

        """
        self._check_metadata_uri()
        metadata = self._get_blob(schema)
        self._log_metadata(metadata, self._DJ_SCHEMA)

    def persist_schema(self, schema: Any) -> None:
        """
        Persist an inferred schema produced by a validation framework.

        Parameters
        ----------
        schema : Any
            An inferred schema object produced by a validation library.

        """
        rendered = self.plugin_handler.render_schema(schema)
        for obj in rendered:
            self.persist_artifact(obj.object,
                                  obj.filename)

    # Validation

    def validate_wrapper(self,
                         constraints: Optional[dict] = None,
                         validation_kwargs: Optional[dict] = None) -> Any:
        """
        Execute validation of a resource.

        Parameters
        ----------
        constraints : dict, default = None
            Constraints from configuration.
        validation_kwargs : dict, default = None
            Mappers for specific framework arguments.

        """
        self.fetch_input_data()
        self.fetch_validation_schema()
        return self.plugin_handler.validate(
                                    self.run_info.data_resource.get("name"),
                                    self._data,
                                    constraints,
                                    self._val_schema,
                                    validation_kwargs)
      
    def validate_datajudge(self,
                           constraints: Optional[dict] = None,
                           validation_kwargs: Optional[dict] = None
                           ) -> dict:
        """
        Produce datajudge validation report.

        Parameters
        ----------
        constraints : dict, default = None
            Constraints from configuration.
        validation_kwargs : dict, default = None
            Mappers for specific framework arguments

        """
        report = self.validate_wrapper(constraints, validation_kwargs)
        return self.plugin_handler.produce_report(report)

    def validate(self,
                 constraints: Optional[dict] = None,
                 validation_kwargs: Optional[dict] = None) -> tuple:
        """
        Execute validation over a resource.

        Parameters
        ----------
        constraints : dict, default = None
            Constraints from configuration.
        validation_kwargs : dict, default = None
            Mappers for specific framework arguments.

        """
        report = self.validate_wrapper(constraints, validation_kwargs)
        report_dj = self.validate_datajudge()
        return report, report_dj
      
    def log_report(self, report: dict) -> None:
        """
        Log short report.

        Parameters
        ----------
        report : dict
            A datajudge report to be logged.

        """
        self._check_metadata_uri()
        metadata = self._get_blob(report)
        self._log_metadata(metadata, self._DJ_REPORT)

    def persist_report(self, report: Any) -> None:
        """
        Persist a report produced by a validation framework.

        Parameters
        ----------
        report : Any
            An report object produced by a validation library.

        """
        rendered = self.plugin_handler.render_report(report)
        for obj in rendered:
            self.persist_artifact(obj.object,
                                  obj.filename)

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
        self.fetch_input_data()
        return self.plugin_handler.profile(self.run_info.data_resource.get("name"),
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
        profile = self.profile_wrapper(profiler_kwargs)
        return self.plugin_handler.produce_profile(profile)

    def profile(self,
                profiler_kwargs: Optional[dict] = None) -> tuple:
        """
        Execute profiling over a resource.
       
        Parameters
        ----------
        profiler_kwargs : dict, default = None
            Mappers for specific framework arguments.

        """
        profile = self.profile_wrapper(profiler_kwargs)
        profile_dj = self.profile_datajudge()
        return profile, profile_dj

    def log_profile(self, profile: dict) -> None:
        """
        Log a data profile.

        Parameters
        ----------
        profile : Any
            A datajudge profile to be logged.

        """
        self._check_metadata_uri()
        metadata = self._get_blob(profile)
        self._log_metadata(metadata, self._DJ_PROFILE)

    def persist_profile(self, profile: Any) -> None:
        """
        Persist a data profile produced by a profiling framework.

        Parameters
        ----------
        profile : Any
            A profile object produced by a profiling library.

        """
        rendered = self.plugin_handler.render_profile(profile)
        for obj in rendered:
            self.persist_artifact(obj.object,
                                  obj.filename)

    # Input data

    def fetch_input_data(self) -> str:
        """
        Fetch data from backend and return temp file path.
        """
        if self._data is None:
            path = self.run_info.data_resource.get("path")
            if isinstance(path, list):
                self._data = [self.fetch_artifact(i) for i in path]
            else:
                self._data = self.fetch_artifact(path)
        return self._data

    def fetch_validation_schema(self) -> str:
        """
        Fetch validation schema from backend and return temp file path.
        """
        if self.run_info.data_resource.get("schema") is None:
            return
        if self._val_schema is None:
            self._val_schema = self.fetch_artifact(
                self.run_info.data_resource.get("schema"))
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
