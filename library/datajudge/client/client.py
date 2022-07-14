"""
Client module.
Implementation of a Client object to interact with storages
and create runs.
"""

from __future__ import annotations

import typing
from typing import List, Optional, Union

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
    The Client constructor build a StoreHandler to keep track of stores,
    both metadata and artifact, and a RunBuilder to create runs.
    All the parameters passed to the Client interface are passed to the
    StoreHandler.

    Parameters
    ----------
    metadata_store : Optional[StoreConfig], optional
        StoreConfig containing configuration for the metadata store, by default None.
    store : Optional[Union[StoreConfig, List[StoreConfig]]], optional
        (List of) StoreConfig containing configuration for the artifact stores, by default None.
    project : Optional[str], optional
        The id of the project, required for the DigitalHub metadata store, by default "project".
    tmp_dir : Optional[str], optional
        Default local temporary folder where to store input data, by default "./djruns/tmp".

    Methods
    -------
    add_store
        Add a new store to the client internal registry.
    create_run
        Create a new run.

    """

    def __init__(self,
                 metadata_store: Optional[StoreConfig] = None,
                 store: Optional[Union[StoreConfig, List[StoreConfig]]] = None,
                 project: Optional[str] = "project",
                 tmp_dir: Optional[str] = "./djruns/tmp"
                 ) -> None:
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
        resources : Union[List[DataResource], DataResource]
            (List of) DataResource object(s).
        run_config : RunConfig
            RunConfig object.
        experiment : Optional[str], optional
            Name of the experiment. An experiment is a logical unit for ordering the runs execution, by default "experiment".
        run_id : Optional[str], optional
            Optional string parameter for user defined run id, by default None.
        overwrite : Optional[bool], optional
            If True, the run metadata/artifact can be overwritten by a run with the same id, by default False.

        Returns
        -------
        Run
            Run object.
        """
        return self._run_builder.create_run(resources,
                                            run_config,
                                            experiment,
                                            run_id,
                                            overwrite)
