"""
Run module.
"""
from __future__ import annotations

import typing
from pathlib import Path
from typing import Any, List, Optional

from datajudge.data import BlobLog, EnvLog
from datajudge.utils.commons import (DATAJUDGE_VERSION, MT_ARTIFACT_METADATA,
                                     MT_DJ_PROFILE, MT_DJ_REPORT, MT_DJ_SCHEMA,
                                     MT_RUN_ENV, MT_RUN_METADATA, STATUS_ERROR,
                                     STATUS_FINISHED, STATUS_INIT,
                                     STATUS_INTERRUPTED)
from datajudge.utils.exceptions import StoreError
from datajudge.utils.uri_utils import get_name_from_uri
from datajudge.utils.utils import get_time, listify

if typing.TYPE_CHECKING:
    from datajudge.client.client import Client
    from datajudge.data.datajudge_profile import DatajudgeProfile
    from datajudge.data.datajudge_report import DatajudgeReport
    from datajudge.data.datajudge_schema import DatajudgeSchema
    from datajudge.run.run_handler import RunHandler
    from datajudge.run.run_info import RunInfo
    from datajudge.utils.config import Constraint
    

class Run:
    """
    Run object.
    The Run is the main interface to interact with data,
    metadata and operational framework. With the Run, you
    can infer, validate and profile resources, log and
    persist data and metadata.

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
    persist_data :
        Persist input data into default store.
    fetch_data :
        Fetch input data from artifact store.

    """

    # Constructor

    def __init__(self,
                 run_info: RunInfo,
                 run_handler: RunHandler,
                 client: Client,
                 overwrite: bool) -> None:

        self.run_info = run_info
        self._client = client
        self._run_handler = run_handler
        self._overwrite = overwrite

        self._filenames = {}

    # Run methods

    def _log_run(self) -> None:
        """
        Log run's metadata.
        """
        metadata = self._get_blob(self.run_info.to_dict())
        self._log_metadata(metadata, MT_RUN_METADATA)

    def _log_env(self) -> None:
        """
        Log run's enviroment details.
        """
        env_data = EnvLog().to_dict()
        metadata = self._get_blob(env_data)
        self._log_metadata(metadata, MT_RUN_ENV)

    def _get_blob(self,
                  content: Optional[dict] = None) -> dict:
        """
        Return structured content to log.
        """
        if content is None:
            content = {}
        return BlobLog(self.run_info.run_id,
                       self.run_info.experiment_name,
                       DATAJUDGE_VERSION,
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
        self._log_metadata(metadata, MT_ARTIFACT_METADATA)

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

    def _persist_artifact(self,
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
        self._check_artifacts_uri()
        if metadata is None:
            metadata = {}
        self._client.persist_artifact(src,
                                      self.run_info.run_artifacts_uri,
                                      src_name=src_name,
                                      metadata=metadata)
        self._log_artifact(src_name)

    def _fetch_data(self) -> None:
        """
        Fetch data from backend and return temp file path.
        """
        for res in self.run_info.resources:
            if res.tmp_pth is None:
                if isinstance(res.path, list):
                    res.tmp_pth = [self._fetch_artifact(i, res.store)
                                   for i in res.path]
                else:
                    res.tmp_pth = self._fetch_artifact(res.path, res.store)

    def _fetch_artifact(self,
                       uri: str,
                       store_name: Optional[str] = None) -> str:
        """
        Fetch artifact from backend.

        Parameters
        ----------
        uri : str
            URI of artifact to fetch.
        store_name : str
            Name of store where to fetch data.

        """
        self._check_artifacts_uri()
        return self._client.fetch_artifact(uri, store_name)

    def _check_metadata_uri(self) -> None:
        """
        Check metadata uri existence.
        """
        if self.run_info.run_metadata_uri is None:
            raise StoreError("Please configure a metadata store.")

    def _check_artifacts_uri(self) -> None:
        """
        Check artifact uri existence.
        """
        if self.run_info.run_artifacts_uri is None:
            raise StoreError("Please configure a artifact store.")

    # Inference

    def infer_wrapper(self) -> List[Any]:
        """
        Execute schema inference on resources.
        """
        schemas = self._run_handler.get_artifact_schema()
        if schemas:
            return schemas
        self._fetch_data()
        self._run_handler.infer(self.run_info.resources)
        return self._run_handler.get_artifact_schema()

    def infer_datajudge(self) -> List[DatajudgeSchema]:
        """
        Produce datajudge inference schema.
        """
        schemas = self._run_handler.get_datajudge_schema()
        if schemas:
            return schemas
        self._fetch_data()
        self._run_handler.infer(self.run_info.resources)
        return self._run_handler.get_datajudge_schema()

    def infer(self,
              only_dj: bool = False) -> Any:
        """
        Execute schema inference on resources.
        """
        schema = self.infer_wrapper()
        schema_dj = self.infer_datajudge()
        if only_dj:
            return None, schema_dj
        return schema, schema_dj

    def log_schema(self) -> None:
        """
        Log datajudge schema.
        """
        self._check_metadata_uri()
        objects = self._run_handler.get_datajudge_schema()
        for obj in objects:
            metadata = self._get_blob(obj.to_dict())
            self._log_metadata(metadata, MT_DJ_SCHEMA)

    def persist_schema(self) -> None:
        """
        Persist an inferred schema produced by a validation framework.
        """
        objects = self._run_handler.get_rendered_schema()
        for obj in objects:
            self._persist_artifact(obj.object,
                                  self._render_artifact_name(obj.filename))

    # Validation

    def validate_wrapper(self,
                         constraints: List[Constraint]
                         ) -> Any:
        """
        Execute validation on resources.

        Parameters
        ----------
        constraints : dict
            List of constraint to validate resources.

        """
        reports = self._run_handler.get_artifact_report()
        if reports:
            return reports
        self._fetch_data()
        self._run_handler.validate(self.run_info.resources,
                                   constraints)
        return self._run_handler.get_artifact_report()

    def validate_datajudge(self,
                           constraints: List[Constraint]
                           ) -> List[DatajudgeReport]:
        """
        Produce datajudge validation report.

        Parameters
        ----------
        constraints : dict, default = None
            List of constraint to validate resources.

        """
        reports = self._run_handler.get_datajudge_report()
        if reports:
            return reports
        self._fetch_data()
        self._run_handler.validate(self.run_info.resources,
                                   constraints)
        return self._run_handler.get_datajudge_report()

    def validate(self,
                 constraints: List[Constraint],
                 only_dj: bool = False
                 ) -> Any:
        """
        Execute validation on resources.

        Parameters
        ----------
        constraints : dict, default = None
            List of constraint to validate resources.

        """
        report = self.validate_wrapper(constraints)
        report_dj = self.validate_datajudge(constraints)
        if only_dj:
            return None, report_dj
        return report, report_dj

    def log_report(self) -> None:
        """
        Log short report.
        """
        self._check_metadata_uri()
        objects = self._run_handler.get_datajudge_report()
        for obj in objects:
            metadata = self._get_blob(obj.to_dict())
            self._log_metadata(metadata, MT_DJ_REPORT)

    def persist_report(self) -> None:
        """
        Persist a report produced by a validation framework.
        """
        objects = self._run_handler.get_rendered_report()
        for obj in objects:
            self._persist_artifact(obj.object,
                                  self._render_artifact_name(obj.filename))

    # Profiling

    def profile_wrapper(self) -> List[Any]:
        """
        Execute profiling on resources.
        """
        profiles = self._run_handler.get_artifact_profile()
        if profiles:
            return profiles
        self._fetch_data()
        self._run_handler.profile(self.run_info.resources)
        return self._run_handler.get_artifact_profile()

    def profile_datajudge(self) -> List[DatajudgeProfile]:
        """
        Produce datajudge profiling report.
        """
        profiles = self._run_handler.get_datajudge_profile()
        if profiles:
            return profiles
        self._fetch_data()
        self._run_handler.profile(self.run_info.resources)
        return self._run_handler.get_datajudge_profile()

    def profile(self,
                only_dj: bool = False
                ) -> Any:
        """
        Execute profiling on resources.
        """
        profile = self.profile_wrapper()
        profile_dj = self.profile_datajudge()
        if only_dj:
            return None, profile_dj
        return profile, profile_dj

    def log_profile(self) -> None:
        """
        Log a data profile.
        """
        self._check_metadata_uri()
        objects = self._run_handler.get_datajudge_profile()
        for obj in objects:
            metadata = self._get_blob(obj.to_dict())
            self._log_metadata(metadata, MT_DJ_PROFILE)

    def persist_profile(self) -> None:
        """
        Persist a data profile produced by a profiling framework.
        """
        objects = self._run_handler.get_rendered_profile()
        for obj in objects:
            self._persist_artifact(obj.object,
                                  self._render_artifact_name(obj.filename))

    # Input data persistence
    
    def persist_data(self) -> None:
        """
        Persist input data as artifact.
        """
        self._check_artifacts_uri()
        self._fetch_data()
        for res in self.run_info.resources:
            for path in listify(res.tmp_pth):
                filename = get_name_from_uri(path)
                self._persist_artifact(path, filename)

    # Context manager

    def __enter__(self) -> Run:
        # Set run status
        self.run_info.begin_status = STATUS_INIT
        self.run_info.started = get_time()
        self._log_run()
        self._log_env()
        return self

    def __exit__(self,
                 exc_type,
                 exc_value,
                 traceback) -> None:
        if exc_type is None:
            self.run_info.end_status = STATUS_FINISHED
        elif exc_type in (InterruptedError, KeyboardInterrupt):
            self.run_info.end_status = STATUS_INTERRUPTED
        elif exc_type in (AttributeError, ):
            self.run_info.end_status = STATUS_ERROR
        else:
            self.run_info.end_status = STATUS_ERROR

        self.run_info.finished = get_time()
        self._log_run()

        self._client.clean_all()

    # Dunders

    def __repr__(self) -> str:
        return str(self.run_info.to_dict())
