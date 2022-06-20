"""
Run module.
"""
from __future__ import annotations

import typing
from pathlib import Path
from typing import Any, List, Optional

from datajudge.data import BlobLog, EnvLog
from datajudge.utils.commons import (DATAJUDGE_VERSION, DUMMY_SCHEME, MT_ARTIFACT_METADATA,
                                     MT_DJ_PROFILE, MT_DJ_REPORT, MT_DJ_SCHEMA,
                                     MT_RUN_ENV, MT_RUN_METADATA, STATUS_ERROR,
                                     STATUS_FINISHED, STATUS_INIT,
                                     STATUS_INTERRUPTED)
from datajudge.utils.exceptions import StoreError
from datajudge.utils.utils import LOGGER, get_time

if typing.TYPE_CHECKING:
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
                 overwrite: bool) -> None:

        self.run_info = run_info
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

    def _get_dict(self, obj: Any) -> dict:
        """
        Transform datajudge reports in dictionary.
        """
        try:
            return obj.to_dict()
        except TypeError:
            LOGGER.error("Failed to convert result in dictionary. ",
                         "Check logs for more infos.")

    def _log_metadata(self,
                      metadata: dict,
                      src_type: str) -> None:
        """
        Log generic metadata.
        """
        self._run_handler.log_metadata(
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
        self._run_handler.persist_artifact(src,
                                           self.run_info.run_artifacts_uri,
                                           src_name=src_name,
                                           metadata=metadata)
        self._log_artifact(src_name)

    def _check_metadata_uri(self) -> None:
        """
        Check metadata uri existence.
        """
        if self.run_info.run_metadata_uri in DUMMY_SCHEME:
            raise StoreError("Please configure a metadata store.")

    def _check_artifacts_uri(self) -> None:
        """
        Check artifact uri existence.
        """
        if self.run_info.run_artifacts_uri in DUMMY_SCHEME:
            raise StoreError("Please configure a artifact store.")

    def _get_libraries(self) -> None:
        """
        Return the list of libraries used by the run.
        """
        self.run_info.run_libraries = self._run_handler.get_libraries()

    # Inference

    def infer_wrapper(self,
                      parallel: bool = False,
                      num_worker: int = 10) -> List[Any]:
        """
        Execute schema inference on resources.
        """
        schemas = self._run_handler.get_artifact_schema()
        if schemas:
            return schemas

        self._run_handler.infer(self.run_info.resources,
                                parallel,
                                num_worker)
        return self._run_handler.get_artifact_schema()

    def infer_datajudge(self,
                        parallel: bool = False,
                        num_worker: int = 10) -> List[DatajudgeSchema]:
        """
        Produce datajudge inference schema.
        """
        schemas = self._run_handler.get_datajudge_schema()
        if schemas:
            return schemas

        self._run_handler.infer(self.run_info.resources,
                                parallel,
                                num_worker)
        return self._run_handler.get_datajudge_schema()

    def infer(self,
              parallel: bool = False,
              num_worker: int = 10,
              only_dj: bool = False) -> Any:
        """
        Execute schema inference on resources.
        """
        schema = self.infer_wrapper(parallel,
                                    num_worker)
        schema_dj = self.infer_datajudge(parallel,
                                         num_worker)
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
            dict_obj = self._get_dict(obj)
            metadata = self._get_blob(dict_obj)
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
                         constraints: List[Constraint],
                         parallel: bool = False,
                         num_worker: int = 10
                         ) -> List[Any]:
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

        self._run_handler.validate(self.run_info.resources,
                                   constraints,
                                   parallel,
                                   num_worker)
        return self._run_handler.get_artifact_report()

    def validate_datajudge(self,
                           constraints: List[Constraint],
                           parallel: bool = False,
                           num_worker: int = 10
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

        self._run_handler.validate(self.run_info.resources,
                                   constraints,
                                   parallel,
                                   num_worker)
        return self._run_handler.get_datajudge_report()

    def validate(self,
                 constraints: List[Constraint],
                 parallel: bool = False,
                 num_worker: int = 10,
                 only_dj: bool = False
                 ) -> Any:
        """
        Execute validation on resources.

        Parameters
        ----------
        constraints : dict, default = None
            List of constraint to validate resources.

        """
        report = self.validate_wrapper(constraints,
                                       parallel,
                                       num_worker)
        report_dj = self.validate_datajudge(constraints,
                                            parallel,
                                            num_worker)
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
            dict_obj = self._get_dict(obj)
            metadata = self._get_blob(dict_obj)
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

    def profile_wrapper(self,
                        parallel: bool = False,
                        num_worker: int = 10) -> List[Any]:
        """
        Execute profiling on resources.
        """
        profiles = self._run_handler.get_artifact_profile()
        if profiles:
            return profiles

        self._run_handler.profile(self.run_info.resources,
                                  parallel,
                                  num_worker)
        return self._run_handler.get_artifact_profile()

    def profile_datajudge(self,
                          parallel: bool = False,
                          num_worker: int = 10) -> List[DatajudgeProfile]:
        """
        Produce datajudge profiling report.
        """
        profiles = self._run_handler.get_datajudge_profile()
        if profiles:
            return profiles

        self._run_handler.profile(self.run_info.resources,
                                  parallel,
                                  num_worker)
        return self._run_handler.get_datajudge_profile()

    def profile(self,
                parallel: bool = False,
                num_worker: int = 10,
                only_dj: bool = False
                ) -> Any:
        """
        Execute profiling on resources.
        """
        profile = self.profile_wrapper(parallel,
                                       num_worker)
        profile_dj = self.profile_datajudge(parallel,
                                            num_worker)
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
            dict_obj = self._get_dict(obj)
            metadata = self._get_blob(dict_obj)
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

    def persist_data(self,
                     file_format: Optional[str] = "parquet") -> None:
        """
        Persist input data as artifact.
        Depending on the functioning of the store object on which the
        artifacts are stored, the store will try to download the data
        locally in the format requested by the user. If the specific
        format is not managed by the store, the store will persist the
        data in a default format.

        In the case of SQL/ODBC storage, the format will be parquet.
        In the case of remote/REST/local stores, the persistence format
        will be the same as the artifacts present in the storage.

        Finally, note that some stores (S3 and Azure) provide for the
        possibility of building presigned URLs by specifying a format
        ('s3' and 'azure' respectively).
        By selecting this specific type of format, it will not be possible
        to persist the data.

        Parameters
        ----------
        format : str
            Format with which to persist input data.

        """
        self._check_artifacts_uri()
        self._run_handler.persist_data(self.run_info.resources,
                                       file_format,
                                       self.run_info.run_artifacts_uri)

    # Context manager

    def __enter__(self) -> Run:
        # Set run status
        LOGGER.info(f"Starting run {self.run_info.run_id}")
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

        self._get_libraries()
        self.run_info.finished = get_time()
        self._log_run()
        LOGGER.info(f"Run finished. Clean up of temp resources.")

        self._run_handler.clean_all()

    # Dunders

    def __repr__(self) -> str:
        return str(self.run_info.to_dict())
