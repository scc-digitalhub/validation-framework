"""
Client module.
Implementation of a Client object to interact with storages
and create runs.
"""
from __future__ import annotations

import typing
from typing import Any, List, Optional, Union

from datajudge.client.client_handler import ClientHandler

if typing.TYPE_CHECKING:
    from datajudge.data import DataResource
    from datajudge.run import Run
    from datajudge.utils.config import RunConfig, StoreConfig


class Client:
    """
    Client class.

    The Client is a public interface that exposes methods to interact
    with storages and create runs.
    
    The Client has an handler that registers the stores used in the
    experiments.

    Methods
    -------
    add_store :
        Add new artifact store.
    create_run :
        Create a new run.
    log_metadata :
        Log metadata to the metadata store.
    persist_artifact :
        Persist artifact to the artifact store.
    fetch_artifact :
        Fetch artifact from backend storage.

    """

    def __init__(self,
                 metadata_store_config: Optional[List[StoreConfig]] = None,
                 store_configs: Optional[List[StoreConfig]] = None,
                 project_name: Optional[str] = "project",
                 tmp_dir: Optional[str] = "./djruns/tmp"
                 ) -> None:
        """
        Client constructor.

        Parameters
        ----------
        metadata_store_config : StoreConfig or dict or list, default = None
            Dictionary containing configuration for the store.
        stores_config : StoreConfig or dict or list, default = None
            Dictionary containing configuration for the store.
        project_name : str
            The id of the project, needed for the rest metadata store.
        tmp_dir : str
            Default temporary folder where to download data.

        """
        self._client_handler = ClientHandler(project_name,
                                             metadata_store_config,
                                             store_configs,
                                             tmp_dir)

    def add_store(self,
                  config: Union[StoreConfig, dict]
                  ) -> None:
        """
        Add a new store to the client internal registry.

        Parameters
        ----------
        config: StoreConfig or dict

        """
        self._client_handler.add_store(config)

    def create_run(self,
                   resources: Union[List[DataResource], DataResource],
                   run_config: RunConfig,
                   experiment_title: Optional[str] = "experiment",
                   run_id: Optional[str] = None,
                   overwrite: Optional[bool] = False) -> Run:
        """
        Create a new run.

        Parameters
        ----------
        experiment_title : str
            Experiment title. An experiment is a logical unit for ordinate
            runs made on a Data Package/Data Resource.
        data_resource : DataResource
            A DataResource object.
        run_config : RunConfig
            Run configuration object.
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
        return self._client_handler.create_run(resources,
                                               run_config,
                                               experiment_title,
                                               run_id,
                                               overwrite)

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
        self._client_handler.log_metadata(metadata, dst, src_type, overwrite)

    def persist_artifact(self,
                         src: Any,
                         dst: str,
                         src_name: str,
                         metadata: dict
                         ) -> None:
        """
        Method to persist artifacts in the default artifact store.

        Parameters
        ----------
        src : str, list or dict
            One or a list of URI described by a string, or a dictionary.
        dst : str
            URI destination of artifact.
        src_name : str, default = None
            Filename. Required only if src is a dictionary.
        metadata: dict, default = None
            Optional metadata to attach on artifact.

        """
        self._client_handler.persist_artifact(src, dst, src_name, metadata)

    def fetch_artifact(self,
                       uri: str,
                       store_name: Optional[str] = None) -> str:
        """
        Fetch artifact from backend and store locally.

        Parameters
        ----------
        uri : str
            URI of artifact to fetch.
        store_name : str, default = None
            Store name where to fetch an artifact.

        Returns
        -------
        str :
            Path to temp file

        """
        return self._client_handler.fetch_artifact(uri, store_name)
