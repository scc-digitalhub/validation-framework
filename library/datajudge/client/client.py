"""
Client module.
Implementation of a Client object to interact with storages
and create runs.
"""
# pylint: disable=import-error,too-many-arguments
from __future__ import annotations

import typing
from typing import Any, List, Optional, Union

from slugify import slugify

from datajudge.utils import config as cfg
from datajudge.utils.factories import get_md_store, get_stores, get_run

# For type checking -> avoids circular imports
if typing.TYPE_CHECKING:
    from datajudge.data import DataResource
    from datajudge.run import Run
    from datajudge.utils.config import RunConfig


store_cfg = Optional[List[Union[cfg.StoreConfig, dict]]]


class Client:
    """
    Client class.

    The Client allows interaction with storages and create runs.
    It builds three storages, one for metadata and two for artifacts.

    Metadata are a collection of data describing runs, data resources/packages,
    reports, schemas, profiling and artifacts metadata.

    Artifacts are files or objects. They can be input data/validation schemas,
    output file produced by the run, like reports, data profiles, etc.

    Methods
    -------
    create_run :
        Create a new run.
    log_metadata :
        Log metadata to the metadata store.
    persist_artifact :
        Persist artifact to the artifact store.
    fetch_artifact :
        Fetch artifact from backend storage.
    get_data_resource_uri :
        Return the URI of a Data Resource.

    """

    def __init__(self,
                 project_name: Optional[str] = cfg.DEFAULT_PROJ,
                 metadata_store_config: store_cfg = cfg.DEFAULT_MD_STORE,
                 store_configs: store_cfg = cfg.DEFAULT_STORE,
                 tmp_dir: Optional[str] = cfg.DEFAULT_TMP
                 ) -> None:
        """
        Client constructor.

        Parameters
        ----------
        project_name : str
            The id of the project, needed for the rest metadata store.
        metadata_store_config : StoreConfig or dict or list, default = StoreConfig
            Dictionary containing configuration for the store.
        stores_config : StoreConfig or dict or list, default = StoreConfig
            Dictionary containing configuration for the store.
        tmp_dir : str
            Default temporary folder where to download data.

        """
        self._project_name = project_name
        self._metadata_store = get_md_store(self._project_name,
                                            metadata_store_config)
        self._store_registry = get_stores(store_configs)
        self._default_store = self._select_default_store()
        self._tmp_dir = tmp_dir

    def _select_default_store(self) -> None:
        """
        Select default store in the store registry.
        """
        if len(self._store_registry) == 1:
            key = next(iter(self._store_registry))
            return self._store_registry.get(key).get("store")

        default = None
        for _, v in self._store_registry.items():
            if v.get("is_default", False):
                if default is None:
                    default = v.get("store")
                else:
                    raise ValueError("Please configure only one store as default.")
        if default is None:
            raise ValueError("Please configure one store as default.")
        return default

    def add_store(self, 
                  config: Union[cfg.StoreConfig, dict]
                  ) -> None:
        """
        Add a new store to the client internal registry.

        Parameters
        ----------
        config: StoreConfig or dict

        """
        dict_store = get_stores(config)
        key = next(iter(dict_store))
        if key in self._store_registry:
            raise ValueError("There is already a store with that name. " +
                             "Please choose another.")

        self._store_registry[key] = dict_store[key]

    def create_run(self,
                   data_resource: DataResource,
                   run_config: RunConfig,
                   experiment_title: Optional[str] = cfg.DEFAULT_EXP,
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
        experiment_name = slugify(experiment_title,
                                  max_length=20,
                                  separator="_")

        run_id = self._metadata_store.get_run_id(run_id)

        self._metadata_store.init_run(experiment_name,
                                      run_id, 
                                      overwrite)

        run_metadata_uri = self._metadata_store.get_run_metadata_uri(experiment_name,
                                                                     run_id)
        run_artifacts_uri = self._default_store.get_run_artifacts_uri(experiment_name,
                                                                      run_id)

        run_info_args = (experiment_title,
                         experiment_name,
                         run_id,
                         run_config,
                         run_metadata_uri,
                         run_artifacts_uri)

        run = get_run(run_info_args,
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
        self._default_store.persist_artifact(src, dst, src_name, metadata)

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
        if store_name is None:
            in_store = self._default_store
        else:
            in_store = self._store_registry.get(store_name).get("store")
        return in_store.fetch_artifact(uri, self.tmp_dir)

    def get_data_resource_uri(self,
                              exp_name: str,
                              run_id: str) -> str:
        """
        Method that wrap 'get_data_resource_uri' of the
        metadata store. Return DataResource URI.
        """
        return self._metadata_store.get_data_resource_uri(exp_name,
                                                          run_id)

    @property
    def tmp_dir(self) -> str:
        """
        Return temporary dir name.
        """
        return self._tmp_dir

    def __repr__(self) -> str:
        return str(self.__dict__)
