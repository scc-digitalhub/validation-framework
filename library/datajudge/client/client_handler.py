"""
ClientHandler module.
"""
# pylint: disable=raise-missing-from,too-many-arguments
from __future__ import annotations

import typing
from typing import Any, List, Optional, Union

from datajudge.client.store_factory import StoreBuilder
from datajudge.data import DataResource
from datajudge.run import Run, RunHandler, RunInfo
from datajudge.utils.config import RunConfig, StoreConfig
from datajudge.utils.exceptions import StoreError
from datajudge.utils.file_utils import clean_all
from datajudge.utils.utils import get_uiid, listify

if typing.TYPE_CHECKING:
    from datajudge.store_artifact.artifact_store import ArtifactStore
    from datajudge.store_metadata.metadata_store import MetadataStore


STORE_TYPE_ARTIFACT = "artifact_store"
DEFAULT_STORE = "default_store"
STORE_TYPE_METADATA = "metadata_store"


class ClientHandlerStoreRegistry:
    """
    Registry where to register Stores by type.
    """

    def __init__(self) -> None:
        self._registry = {}
        self.setup()

    def setup(self) -> None:
        """
        Setup basic registry.
        """
        self._registry[STORE_TYPE_ARTIFACT] = []
        self._registry[DEFAULT_STORE] = None
        self._registry[STORE_TYPE_METADATA] = None

    def register(self,
                 store: dict,
                 store_type: str) -> None:
        """
        Register a new store.
        """
        if store_type == STORE_TYPE_ARTIFACT:
            self._registry[store_type].append(store)
        else:
            self._registry[store_type] = store

    def update_default_store(self) -> None:
        """
        Select default store in the store registry.

        Raise if there are no store to choose from. If only one store is
        provided, that one is choosed as default. If multiple stores are
        provided, only one store MUST be configured as isDefault.

        When you configure a client without artifact store configuration, the
        default store is a Dummy store. There is no option to update the
        default store after the client initialization, so, if you do not flag a
        store as default, you loose the abilty to persist artifact into a
        backend.

        """
        stores = self._registry[STORE_TYPE_ARTIFACT]
        default = None

        if not stores:
            raise StoreError("Configure at least one store.")

        if len(stores) == 1:
            default = stores[0]
            default["is_default"] = True
            self.register(default, DEFAULT_STORE)
            return

        for store in stores:
            if store.get("is_default", False):
                if default is None:
                    default = store
                    self.register(default, DEFAULT_STORE)
                else:
                    raise StoreError("Configure only one store as default.")

        try:
            assert default["is_default"]
        except AssertionError:
            raise StoreError("Please configure one store as default.")

    def get_store(self,
                  store_type: str,
                  store_name: Optional[str] = None) -> Any:
        """
        Return a store from registry.
        """
        if store_type in (STORE_TYPE_METADATA, DEFAULT_STORE):
            return self._registry[store_type]["store"]

        if store_type == STORE_TYPE_ARTIFACT:
            if store_name is not None:
                for store in self._registry[store_type]:
                    if store_name == store.get("name"):
                        return store["store"]
                return None
            return self._registry[DEFAULT_STORE]["store"]

        raise StoreError("Invalid store type.")


class ClientHandler:
    """
    Handler layer between the Client interface, stores and factories.

    The ClientHandler contain a register where it keeps track of stores.

    """
    def __init__(self,
                 metadata_store: Optional[StoreConfig] = None,
                 store: Optional[List[StoreConfig]] = None,
                 project: Optional[str] = "project",
                 tmp_dir: Optional[str] = "./djruns/tmp") -> None:

        self._store_registry = ClientHandlerStoreRegistry()
        self._store_builder = StoreBuilder(project)
        self.setup(metadata_store, store)

        self._tmp_dir = tmp_dir

    def setup(self,
              metadata_store: Optional[StoreConfig] = None,
              store: Optional[List[StoreConfig]] = None
              ) -> None:
        """
        Build stores according to configurations provided
        and register them into the store registry.
        """

        # Build metadata store
        self.add_metadata_store(metadata_store)

        # Build artifact stores
        for cfg in listify(store):
            self.add_artifact_store(cfg)

        # Register default store
        self.add_default_store()

    def add_metadata_store(self,
                           config: Union[StoreConfig, dict]) -> None:
        """
        Add a metadata store to the registry.
        """
        md_store = self._store_builder.build(config, md_store=True)
        self._store_registry.register(md_store, STORE_TYPE_METADATA)

    def add_artifact_store(self,
                           config: Union[StoreConfig, dict]) -> None:
        """
        Add an artifact store to the registry.
        """
        if self.get_art_store(config.name) is None:
            store = self._store_builder.build(config)
            self._store_registry.register(store, STORE_TYPE_ARTIFACT)
        else:
            raise StoreError("There is already a store with that name.\
                              Please choose another name to identify \
                              the store.")

    def add_default_store(self) -> None:
        """
        Add default artifact store to the registry.
        """
        self._store_registry.update_default_store()

    def get_md_store(self) -> MetadataStore:
        """
        Get metadata store from registry.
        """
        return self._store_registry.get_store(STORE_TYPE_METADATA)

    def get_art_store(self, name: str) -> ArtifactStore:
        """
        Get artifact store from registry.
        """
        return self._store_registry.get_store(STORE_TYPE_ARTIFACT, name)

    def get_def_store(self) -> ArtifactStore:
        """
        Get default artifact store from registry.
        """
        return self._store_registry.get_store(DEFAULT_STORE)

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
        if store is not None:
            return store.fetch_artifact(uri, self._tmp_dir)
        raise StoreError(f"No store named {store_name}")

    def _init_run(self,
                  exp_name: str,
                  run_id: str,
                  overwrite: bool) -> None:
        """
        Initialize run in the metadata store backend.
        """
        store = self.get_md_store()
        store.init_run(exp_name, run_id, overwrite)

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

    def create_run(self,
                   resources: Union[List[DataResource], DataResource],
                   run_config: RunConfig,
                   experiment: Optional[str] = "experiment",
                   run_id: Optional[str] = None,
                   overwrite: Optional[bool] = False) -> Run:
        """
        Create a new run.
        """
        resources = listify(resources)
        run_id = get_uiid(run_id)

        self._init_run(experiment, run_id, overwrite)
        run_md_uri = self._get_md_uri(experiment, run_id)
        run_art_uri = self._get_art_uri(experiment, run_id)

        run_handler = RunHandler(run_config)
        run_info = RunInfo(experiment,
                           resources,
                           run_id,
                           run_config,
                           run_md_uri,
                           run_art_uri)
        run = Run(run_info, run_handler, self, overwrite)
        return run

    def clean_all(self) -> None:
        """
        Clean up temp_dir contents.
        """
        try:
            clean_all(self._tmp_dir)
        except FileNotFoundError:
            pass
