from __future__ import annotations

import typing
from typing import Any, Optional

from slugify import slugify  # pylint: disable=import-error

from datajudge.utils.factories import get_stores, get_run_flavour

# For type checking -> avoids circular imports
if typing.TYPE_CHECKING:
    from datajudge.data import DataResource
    from datajudge.run import Run


class Client:
    """
    Client class.

    The Client allows interaction with storages and create runs.
    It builds two storages, one for metadata and another for
    artifacts.
    The metadata are a collection of data describing
    the runs, the data resources/packages, reports and artifacts.
    The artifact can be files, object, dictionaries.

    Attributes
    ----------
    project_id : str, default = 'project'
        The id of the project, needed for the rest metadata store.
    experiment_name : str, default = 'experiment'
        Experiment name. An experiment is a logical unit for keeping
        together the validation runs made on a Data Package/Data Resource.
    metadata_store_uri : str, default = None
        Metadata store URI. The library will select an appropriate
        store object based on the URI scheme.
    metadata_store_config : dict, default = None
        Dictionary containing configuration for the store.
        e.g. credentials, endpoints, etc.
    artifact_store_uri : str, default = None
        Artifact store URI. The library will select an appropriate
        store object based on the URI scheme.
    metadata_store_config : dict, default = None
        Dictionary containing configuration for the store.
        e.g. credentials, endpoints, etc.

    Methods
    -------
    create_run :
        Create a new run.
    log_metadata :
        Log metadata to the metadata store.
    persist_artifact:
        Persist artifact to the srtifact store.

    Notes
    -----
    Although the client exposes methods to log metadata and persist
    artifacts, it's preferrable to use methodes exposed by the Run
    object.

    """

    def __init__(self,
                 project_id: Optional[str] = "project",
                 experiment_name: Optional[str] = "experiment",
                 metadata_store_uri: Optional[str] = None,
                 artifact_store_uri: Optional[str] = None,
                 metadata_store_config: Optional[dict] = None,
                 artifact_store_config: Optional[dict] = None,
                 ) -> None:

        self._project_id = project_id
        self._experiment_name = experiment_name
        self._experiment_id = slugify(experiment_name,
                                      max_length=20,
                                      separator="_")

        self._metadata_store, self._artifact_store = get_stores(
                                                        self._project_id,
                                                        self._experiment_id,
                                                        metadata_store_uri,
                                                        artifact_store_uri,
                                                        metadata_store_config,
                                                        artifact_store_config)

    def create_run(self,
                   data_resource: DataResource,
                   validation_library: str,
                   run_id: Optional[str] = None,
                   overwrite: Optional[bool] = False) -> Run:
        """
        Create a new run.

        Parameters
        ----------
        data_resource : DataResource
            A DataResource object.
        validation_library : str
            Name of the validation framework used to perform
            the validation task. It's used to select a specific
            Run object.
        run_id : str, default = None
            Optional string parameter for user defined run id.
        overwrite : bool, default = False
            If True, the run metadata/artifact can be overwritten
            by a run with the same id.

        Returns
        -------
        Run :
            Return a specific Run object.

        """

        run_id = self._metadata_store.get_run_id(run_id)

        self._metadata_store.init_run(run_id, overwrite)

        run_metadata_uri = self._metadata_store.get_run_metadata_uri(run_id)
        run_artifacts_uri = self._artifact_store.get_run_artifacts_uri(run_id)

        run_info_args = (self._experiment_name,
                         self._experiment_id,
                         run_id,
                         run_metadata_uri,
                         run_artifacts_uri)

        run = get_run_flavour(run_info_args,
                              validation_library,
                              data_resource,
                              self,
                              overwrite)

        return run

    def log_metadata(self,
                     metadata: dict,
                     dst: str,
                     src_type: str,
                     overwrite: bool) -> None:
        """
        Method to log metadata in the metadata store.

        Parameters
        ----------
        metadata : dict
            A dictionary to be logged.
        dst : str
            URI destination of metadata.
        src_type : str
            Metadata type.
        overwrite : bool
            If True, overwrite existent metadata.

        """
        self._metadata_store.log_metadata(metadata,
                                          dst,
                                          src_type,
                                          overwrite)

    def persist_artifact(self,
                         src: Any,
                         dst: str,
                         src_name: Optional[str] = None
                         ) -> None:
        """
        Method to persist artifacts in the artifact store.

        Parameters
        ----------
        src : str, list or dict
            One or a list of URI described by a string, or a dictionary.
        dst : str
            URI destination of artifact.
        src_name : str, default = None
            Filename. Required only if src is a dictionary.

        """
        self._artifact_store.persist_artifact(src, dst, src_name)

    def _get_data_resource_uri(self,
                               run_id: str):
        """
        Method that wrap 'get_data_resource_uri' of the
        metadata store. Return DataREsource URI.
        """
        return self._metadata_store.get_data_resource_uri(run_id)

    def __repr__(self) -> str:
        return str(self.__dict__)
