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

    The Client is a public interface that exposes methods to create
    runs and allows the user to add artifact stores to the pool of runs stores.

    Methods
    -------
    add_store :
        Add new artifact store to the list of stores at runs disposition.
    create_run :
        Create a new run.
    log_metadata :
        Log metadata to the metadata store.
    persist_artifact :
        Persist artifact to a default artifact store.
    fetch_artifact :
        Fetch artifact from backend storages.

    """

    def __init__(self,
                 metadata_store: Optional[StoreConfig] = None,
                 store: Optional[Union[StoreConfig, List[StoreConfig]]] = None,
                 project: Optional[str] = "project",
                 tmp_dir: Optional[str] = "./djruns/tmp"
                 ) -> None:
        """
        The Client constructor build a StoreHandler to keep track of stores,
        both metadata and artifact, and a RunBuilder to create runs.
        All the parameters passed to the Client interface are passed to the
        StoreHandler.

        Parameters
        ----------
        metadata_store : StoreConfig, default = None
            StoreConfig containing configuration for the metadata store.
        store : StoreConfig or List[StoreConfig], default = None
            (List of) StoreConfig containing configuration for the artifact stores.
        project : str
            The id of the project, required for the DigitalHub metadata store.
        tmp_dir : str
            Default local temporary folder where to store input data.

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
            Name of the experiment. An experiment is a logical unit
            for ordering the runs execution.
        data_resource : DataResource or List[DataResource]
            (List of) DataResource object(s).
        run_config : RunConfig
            RunConfig object.
        run_id : str, default = None
            Optional string parameter for user defined run id.
        overwrite : bool, default = False
            If True, the run metadata/artifact can be overwritten
            by a run with the same id.

        Returns
        -------
        Run :
            Return a Run object.

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
        store.fetch_artifact(uri, file_format)
