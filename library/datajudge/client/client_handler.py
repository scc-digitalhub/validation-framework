"""
ClientHandler module.
"""
# pylint: disable=import-error
from __future__ import annotations
from copy import deepcopy

import typing
import uuid
from typing import Any, List, Optional, Tuple, Union

from slugify import slugify

from datajudge.client.store_factories import get_md_store, get_stores
from datajudge.data.data_resource import DataResource
from datajudge.run import Run, RunHandler, RunInfo
from datajudge.utils.config import RunConfig, StoreConfig

if typing.TYPE_CHECKING:
    from datajudge.store_artifact.artifact_store import ArtifactStore
    from datajudge.store_metadata.metadata_store import MetadataStore


STORE_TYPE_ARTIFACT = "artifact_store"
DEFAULT_STORE = "default_artifact_store"
STORE_TYPE_METADATA = "metadata_store"


class ClientHandlerStoreRegistry:
    """
    Registry where to register Stores by type.
    """
    def __init__(self) -> None:
        self.registry = {}
        self.setup()

    def setup(self) -> None:
        """
        Setup basic registry.
        """
        self.registry[STORE_TYPE_ARTIFACT] = []
        self.registry[DEFAULT_STORE] = None
        self.registry[STORE_TYPE_METADATA] = None

    def register(self,
                 store: dict,
                 store_type: str) -> None:
        """
        Register a new store.
        """
        if store_type == STORE_TYPE_ARTIFACT:
            self.registry[STORE_TYPE_ARTIFACT].append(store)
        else:
            self.registry[store_type] = store

    def update_default_store(self) -> None:
        """
        Select default store in the store registry.
        """
        stores = self.registry[STORE_TYPE_ARTIFACT]
        default = None
        
        if len(stores) == 1:
            default = deepcopy(stores[0])
        else:
            for store in stores:
                if store.get("is_default", False):
                    if default is None:
                        default = deepcopy(store)
                    else:
                        raise ValueError("Configure only one store as default.")

        try:
            default.pop("is_default")
            default.pop("name")
        except KeyError:
            pass
        except AttributeError:
            raise RuntimeError("Please configure one store as default.")

        self.register(default, DEFAULT_STORE)

    def get_store(self,
                  store_type: str,
                  name: Optional[str] = None) -> Any:
        """
        Return a store from registry.
        """
        if store_type in (STORE_TYPE_METADATA, DEFAULT_STORE):
            return self.registry[store_type]["store"]

        if store_type == STORE_TYPE_ARTIFACT:
            if name is not None:
                for store in self.registry[STORE_TYPE_ARTIFACT]:
                    if name == store.get("name"):
                        return store["store"]
            return self.registry[DEFAULT_STORE]["store"]


class ClientHandler:
    """
    Handler layer between the Client interface, stores and factories.
    
    The ClientHandler contain a register where it keeps track of stores.

    """

    def __init__(self,
                 md_store_config: Optional[List[StoreConfig]] = None,
                 store_configs: Optional[List[StoreConfig]] = None,
                 project_name: Optional[str] = "project",
                 tmp_dir: Optional[str] = "./djruns/tmp") -> None:
        self._md_store_config = md_store_config
        self._art_store_config = store_configs
        self.proj = project_name
        self.tmp_dir = tmp_dir
        self.store_registry = ClientHandlerStoreRegistry()
        self.setup()

    def setup(self) -> None:
        """
        Setup the registry and register stores according to
        configurations provided.
        """
        md_store = get_md_store(self._md_store_config, self.proj)
        self.store_registry.register(md_store, STORE_TYPE_METADATA)

        stores = get_stores(self._art_store_config)
        for store in stores:
            self.store_registry.register(store, STORE_TYPE_ARTIFACT)
        self.store_registry.update_default_store()

    def get_md_store(self) -> MetadataStore:
        """
        Get metadata store from registry.
        """
        return self.store_registry.get_store(STORE_TYPE_METADATA)

    def get_def_store(self) -> ArtifactStore:
        """
        Get default artifact store from registry.
        """
        return self.store_registry.get_store(DEFAULT_STORE)

    def get_art_store(self, name: str) -> ArtifactStore:
        """
        Get artifact store from registry.
        """
        return self.store_registry.get_store(STORE_TYPE_ARTIFACT, name)

    def add_store(self, config: Union[StoreConfig, dict]) -> None:
        """
        Add an artifact store to the registry.
        """
        store = get_stores(config)
        key = next(iter(store))

        check = self.store_registry.get_store(STORE_TYPE_ARTIFACT, key)
        if check is not None:
            raise ValueError("There is already a store with that name.\
                              Please choose another.")

        self.store_registry.register(store, STORE_TYPE_ARTIFACT)
        self.store_registry.update_default_store()

    def log_metadata(self,
                     src: dict,
                     dst: str,
                     src_type: str,
                     overwrite: bool) -> None:
        """
        Log metadata to the metadata store.
        """
        store = self.get_md_store()
        store.log_metadata(src, dst, src_type, overwrite)

    def persist_artifact(self,
                         src: Any,
                         dst: str,
                         src_name: str,
                         metadata: dict) -> None:
        """
        Persist an artifact in the default store.
        """
        store = self.get_def_store()
        store.persist_artifact(src, dst, src_name, metadata)

    def fetch_artifact(self,
                       uri: str,
                       store_name: Optional[str] = None) -> str:
        """
        Persist an artifact from an artifact store.
        """
        store = self.get_art_store(store_name)
        return store.fetch_artifact(uri, self.tmp_dir)

    @staticmethod
    def _get_run_id(run_id: Optional[str] = None) -> str:
        """
        Return a string UID for a Run.
        """
        if run_id:
            return run_id
        return uuid.uuid4().hex

    def _init_run(self,
                  exp_name: str,
                  run_id: str,
                  overwrite: bool) -> None:
        """
        Initialize run in the metadata store backend.
        """
        store = self.get_md_store()
        store.init_run(exp_name, run_id, overwrite)

    @staticmethod
    def _get_slug(title: str) -> str:
        """
        Slugify a string.
        """
        return slugify(title, max_length=20, separator="_")

    def _get_md_uri(self, exp_name: str, run_id: str) -> str:
        """
        Get the metadata URI store location.
        """
        store = self.get_md_store()
        return store.get_run_metadata_uri(exp_name, run_id)

    def _get_art_uri(self, exp_name: str, run_id: str) -> str:
        """
        Get the artifacts URI store location. It uses the default store.
        """
        store = self.get_def_store()
        return store.get_run_artifacts_uri(exp_name, run_id)

    @staticmethod
    def _listify(obj: Union[List, Tuple, Any]) -> List[Any]:
        """
        Check if an object is a list or a tuple and return a list.
        """
        if not isinstance(obj, (list, tuple)):
            obj = [obj]
        return obj

    def create_run(self,
                   resources: Union[List[DataResource], DataResource],
                   run_config: RunConfig,
                   experiment_title: Optional[str] = "experiment",
                   run_id: Optional[str] = None,
                   overwrite: Optional[bool] = False) -> Run:
        """
        Create a new run.
        """
        resources = self._listify(resources)
        experiment_name = self._get_slug(experiment_title)
        run_id = self._get_run_id(run_id)

        self._init_run(experiment_name, run_id, overwrite)
        run_md_uri = self._get_md_uri(experiment_name, run_id)
        run_art_uri = self._get_art_uri(experiment_name, run_id)

        run_handler = RunHandler(run_config)
        run_info = RunInfo(experiment_title,
                           experiment_name,
                           resources,
                           run_id,
                           run_config,
                           run_md_uri,
                           run_art_uri)
        run = Run(run_info, run_handler, self, overwrite)
        return run
