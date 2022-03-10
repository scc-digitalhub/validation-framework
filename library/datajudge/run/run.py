"""
Run module.
"""
# pylint: disable=import-error,invalid-name,too-many-instance-attributes
from __future__ import annotations

import typing
from pathlib import Path
from typing import Any, List, Optional, Union

from datajudge.data import BlobLog, EnvLog
from datajudge.utils import config as cfg
from datajudge.utils.file_utils import clean_all
from datajudge.utils.uri_utils import get_name_from_uri
from datajudge.utils.utils import data_listify, get_time

if typing.TYPE_CHECKING:
    from datajudge.client import Client
    from datajudge.run import RunInfo, RunHandler
    from datajudge.utils.config import RunConfig


class Run:
    """
    Run object.
    The Run is the main interface to interact with data, metadata and
    operational framework. With the Run, you can infer, validate and profile
    resources, log and persist data and metadata.
    It interacts both with the Client and the Data Resource/resources.

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
    fetch_data :
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
                 plugin_handler: RunHandler,
                 client: Client,
                 overwrite: bool) -> None:

        self.run_info = run_info
        self._client = client
        self._run_handler = plugin_handler
        self._overwrite = overwrite

        self._filenames = {}

    # Run methods

    def _log_run(self) -> None:
        """
        Log run's metadata.
        """
        metadata = self._get_blob(self.run_info.dict())
        self._log_metadata(metadata, self._RUN_METADATA)

    def _log_env(self) -> None:
        """
        Log run's enviroment details.
        """
        env_data = EnvLog().dict()
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
                       content).dict()

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

    def _render_artifact_name(self,
                              filename: str) -> str:
        """
        Return a modified filename to avoid overwriting
        in persistence.
        """
        if filename not in self._filenames:
            self._filenames[filename] = 0
        else:
            self._filenames[filename] += 1

        fnm = Path(filename).stem
        ext = Path(filename).suffix

        return f"{fnm}_{self._filenames[filename]}{ext}"

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
        data = self.fetch_data()
        data, data_name = data_listify(data, data_name)
        for idx, path in enumerate(data):
            # try to infer source name if no name is passed
            src_name = data_name[idx] if data_name[idx] is not None \
                                      else get_name_from_uri(path)
            self.persist_artifact(data[idx], src_name, metadata)

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

    def fetch_data(self) -> None:
        """
        Fetch data from backend and return temp file path.
        """
        for res in self.run_info.resources:
            if res.tmp_pth is None:
                if isinstance(res.path, list):
                    res.tmp_pth = [self.fetch_artifact(i, store_name=res.store)
                                   for i in res.path]
                else:
                    res.tmp_pth = self.fetch_artifact(res.path,
                                                      store_name=res.store)

    def fetch_artifact(self,
                       uri: str,
                       store_name: Optional[str] = None) -> str:
        """
        Fetch artifact from backend.

        Parameters
        ----------
        uri : str
            URI of artifact to fetch.
        """
        self._check_artifacts_uri()
        return self._client.fetch_artifact(uri, store_name)

    def _check_metadata_uri(self) -> None:
        """
        Check metadata uri existence.
        """
        if self.run_info.run_metadata_uri is None:
            raise AttributeError("Please configure a metadata store.")

    def _check_artifacts_uri(self) -> None:
        """
        Check artifact uri existence.
        """
        if self.run_info.run_artifacts_uri is None:
            raise AttributeError("Please configure a artifact store.")

    # Inference

    def infer_wrapper(self,
                      exec_args: Optional[dict] = None) -> Any:
        """
        Execute schema inference over a resource.

        Parameters
        ----------
        exec_args : dict, default = None
            Mappers for specific framework arguments.

        """
        schemas = self._run_handler.get_result_schema()
        if schemas:
            return schemas
        self.fetch_data()
        self._run_handler.infer(self.run_info.resources, exec_args)
        return self._run_handler.get_result_schema()

    def infer_datajudge(self,
                        exec_args: Optional[dict] = None) -> dict:
        """
        Produce datajudge inference schema.

        Parameters
        ----------
        exec_args : dict, default = None
            Mappers for specific framework arguments.

        """
        schemas = self._run_handler.get_datajudge_schema()
        if schemas:
            return schemas
        self.fetch_data()
        self._run_handler.infer(self.run_info.resources, exec_args)
        return self._run_handler.get_datajudge_schema()

    def infer(self,
              exec_args: Optional[dict] = None) -> tuple:
        """
        Execute schema inference over a resource.

        Parameters
        ----------
        exec_args : dict, default = None
            Mappers for specific framework arguments.

        """
        schema = self.infer_wrapper(exec_args)
        schema_dj = self.infer_datajudge(exec_args)
        return schema, schema_dj

    def log_schema(self) -> None:
        """
        Log datajudge schema.
        """
        self._check_metadata_uri()
        objects = self._run_handler.get_datajudge_schema()
        for obj in objects:
            metadata = self._get_blob(obj.dict())
            self._log_metadata(metadata, self._DJ_SCHEMA)

    def persist_schema(self) -> None:
        """
        Persist an inferred schema produced by a validation framework.
        """
        objects = self._run_handler.get_artifact_schema()
        for obj in objects:
            self.persist_artifact(obj.object,
                                  self._render_artifact_name(obj.filename))

    # Validation

    def validate_wrapper(self,
                         constraints: RunConfig,
                         exec_args: Optional[dict] = None) -> Any:
        """
        Execute validation of a resource.

        Parameters
        ----------
        constraints : dict
            Constraints from configuration.
        exec_args : dict, default = None
            Mappers for specific framework arguments.

        """
        reports = self._run_handler.get_result_report()
        if reports:
            return reports
        self.fetch_data()
        self._run_handler.validate(self.run_info.resources,
                                   constraints, exec_args)
        return self._run_handler.get_result_report()

    def validate_datajudge(self,
                           constraints: Optional[dict] = None,
                           exec_args: Optional[dict] = None
                           ) -> dict:
        """
        Produce datajudge validation report.

        Parameters
        ----------
        constraints : dict, default = None
            Constraints from configuration.
        exec_args : dict, default = None
            Mappers for specific framework arguments

        """
        reports = self._run_handler.get_datajudge_report()
        if reports:
            return reports
        self.fetch_data()
        self._run_handler.validate(self.run_info.resources,
                                   constraints, exec_args)
        return self._run_handler.get_datajudge_report()

    def validate(self,
                 constraints: Optional[dict] = None,
                 exec_args: Optional[dict] = None) -> tuple:
        """
        Execute validation over a resource.

        Parameters
        ----------
        constraints : dict, default = None
            Constraints from configuration.
        exec_args : dict, default = None
            Mappers for specific framework arguments.

        """
        report = self.validate_wrapper(constraints, exec_args)
        report_dj = self.validate_datajudge(constraints, exec_args)
        return report, report_dj

    def log_report(self) -> None:
        """
        Log short report.
        """
        self._check_metadata_uri()
        objects = self._run_handler.get_datajudge_report()
        for obj in objects:
            metadata = self._get_blob(obj.dict())
            self._log_metadata(metadata, self._DJ_REPORT)

    def persist_report(self) -> None:
        """
        Persist a report produced by a validation framework.
        """
        objects = self._run_handler.get_artifact_report()
        for obj in objects:
            self.persist_artifact(obj.object,
                                  self._render_artifact_name(obj.filename))

    # Profiling

    def profile_wrapper(self,
                        exec_args: dict = None) -> List[Any]:
        """
        Execute profiling on a resource.

        Parameters
        ----------
        exec_args : dict, default = None
            Kwargs passed to profiler.

        """
        profiles = self._run_handler.get_result_profile()
        if profiles:
            return profiles
        self.fetch_data()
        self._run_handler.profile(self.run_info.resources, exec_args)
        return self._run_handler.get_result_profile()

    def profile_datajudge(self,
                          exec_args: dict = None
                          ) -> List[Any]:
        """
        Execute schema inference over a resource.
        Return the schema inferred by datajudge.

        Parameters
        ----------
        exec_args : dict, default = None
            Kwargs passed to profiler.

        """
        profiles = self._run_handler.get_datajudge_profile()
        if profiles:
            return profiles
        self.fetch_data()
        self._run_handler.profile(self.run_info.resources, exec_args)
        return self._run_handler.get_datajudge_profile()

    def profile(self,
                exec_args: Optional[dict] = None) -> tuple:
        """
        Execute profiling over a resource.

        Parameters
        ----------
        exec_args : dict, default = None
            Mappers for specific framework arguments.

        """
        profile = self.profile_wrapper(exec_args)
        profile_dj = self.profile_datajudge(exec_args)
        return profile, profile_dj

    def log_profile(self) -> None:
        """
        Log a data profile.
        """
        self._check_metadata_uri()
        objects = self._run_handler.get_datajudge_profile()
        for obj in objects:
            metadata = self._get_blob(obj.dict())
            self._log_metadata(metadata, self._DJ_PROFILE)

    def persist_profile(self) -> None:
        """
        Persist a data profile produced by a profiling framework.
        """
        objects = self._run_handler.get_artifact_profile()
        for obj in objects:
            self.persist_artifact(obj.object,
                                  self._render_artifact_name(obj.filename))

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
        return str(self.run_info.dict())
