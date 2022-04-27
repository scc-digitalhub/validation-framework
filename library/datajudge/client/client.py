"""
Client module.
Implementation of a Client object to interact with storages
and create runs.
"""
# pylint: disable=raise-missing-from,too-many-arguments
from __future__ import annotations

import typing
from typing import Any, List, Optional, Union

from datajudge.client.store_handler import StoreHandler
from datajudge.client.run_builder import RunBuilder

if typing.TYPE_CHECKING:
    from datajudge.data import DataResource
    from datajudge.run import Run
    from datajudge.utils.config import RunConfig, StoreConfig


class Client:
    """
    Client class.

    The Client is a public interface that exposes methods to interact
    with storages and create runs.

    The Client has an handler that registers the stores used in runs and
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
                 metadata_store: Optional[List[StoreConfig]] = None,
                 store: Optional[List[StoreConfig]] = None,
                 project: Optional[str] = "project",
                 tmp_dir: Optional[str] = "./djruns/tmp"
                 ) -> None:
        """
        Client constructor. Parameters are passed to a StoreHandler
        constructor that manages Client opration.

        Parameters
        ----------
        metadata_store : StoreConfig or dict or list, default = None
            Dictionary containing configuration for the store.
        store : StoreConfig or dict or list, default = None
            Dictionary containing configuration for the store.
        project : str
            The id of the project, needed for the rest metadata store.
        tmp_dir : str
            Default temporary folder where to download data.

        """
        self._store_handler = StoreHandler(metadata_store,
                                           store,
                                           project,
                                           tmp_dir)
        self._run_builder = RunBuilder(self._store_handler)

    def add_store(self, store: StoreConfig) -> None:
        """
        Add a new store to the client internal registry.

        Parameters
        ----------
        store: StoreConfig
            Store configuration.

        """
        self._store_handler.add_artifact_store(store)

    def create_run(self,
                   resources: Union[List[DataResource], DataResource],
                   run_config: RunConfig,
                   experiment: Optional[str] = "experiment",
                   run_id: Optional[str] = None,
                   overwrite: Optional[bool] = False) -> Run:
        """
        Create a new run.

        Parameters
        ----------
        experiment : str
            Experiment name. An experiment is a logical unit for ordinate
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
        return self._run_builder.create_run(resources,
                                            run_config,
                                            experiment,
                                            run_id,
                                            overwrite)

    def log_metadata(self,
                     src: dict,
                     dst: str,
                     src_type: str,
                     overwrite: bool) -> None:
        """
        Method to log metadata in the metadata store.

        Parameters
        ----------
        src : dict
            A dictionary to be logged.
        dst : str
            URI destination of metadata.
        src_type : str
            Metadata type.
        overwrite : bool
            If True, overwrite existent metadata.

        """
        store = self._store_handler.get_md_store()
        store.log_metadata(src, dst, src_type, overwrite)

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
        store = self._store_handler.get_def_store()
        store.persist_artifact(src, dst, src_name, metadata)

    def fetch_artifact(self,
                       uri: str,
                       file_format: str,
                       store_name: Optional[str] = None) -> str:
        """
        Fetch artifact from backend and store locally.

        Parameters
        ----------
        uri : str
            URI of artifact to fetch.
        format : str
            Format with which to save the data.
        store_name : str, default = None
            Store name where to fetch an artifact. If no name
            is passed, the client uses the default store.

        Returns
        -------
        str :
            Local path to fetched artifact.

        """
        store = self._store_handler.get_art_store(store_name)
        store.fetch_artifact(uri, format)
