"""
StoreHandler module.
"""
# pylint: disable=raise-missing-from,too-many-arguments
from __future__ import annotations

import typing
from typing import Any, List, Optional, Union

from datajudge.client.store_factory import StoreBuilder
from datajudge.utils.config import StoreConfig
from datajudge.utils.exceptions import StoreError
from datajudge.utils.file_utils import clean_all
from datajudge.utils.utils import listify

if typing.TYPE_CHECKING:
    from datajudge.store_artifact.artifact_store import ArtifactStore
    from datajudge.store_metadata.metadata_store import MetadataStore


STORE_TYPE_ARTIFACT = "artifact_store"
DEFAULT_STORE = "default_store"
STORE_TYPE_METADATA = "metadata_store"


class StoreRegistry:
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
            self.registry[store_type].append(store)
        else:
            self.registry[store_type] = store

    def get_store(self,
                  store_type: str,
                  store_name: Optional[str] = None) -> Any:
        """
        Return a store from registry.
        """
        if store_type in (STORE_TYPE_METADATA, DEFAULT_STORE):
            return self.registry[store_type]["store"]

        if store_type == STORE_TYPE_ARTIFACT:
            if store_name is not None:
                for store in self.registry[store_type]:
                    if store_name == store.get("name"):
                        return store["store"]
                return None
            return self.registry[DEFAULT_STORE]["store"]

        raise StoreError("Invalid store type.")

    def get_all_stores(self, store_type: str) -> List[Any]:
        """
        Return all stores by type.
        """
        return self.registry[store_type]


class StoreHandler:
    """
    Handler layer between the Client interface, stores and factories.

    The StoreHandler contain a register where it keeps track of stores.

    """
    def __init__(self,
                 metadata_store: Optional[StoreConfig] = None,
                 store: Optional[List[StoreConfig]] = None,
                 project: Optional[str] = "project",
                 tmp_dir: Optional[str] = "./djruns/tmp") -> None:

        self._store_registry = StoreRegistry()
        self._store_builder = StoreBuilder(project, tmp_dir)
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
        self.update_default_store()

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
        store = self._store_builder.build(config)

        if self.get_art_store(store.get("name")) is None:
            self._store_registry.register(store, STORE_TYPE_ARTIFACT)
        else:
            raise StoreError("There is already a store with that name.\
                              Please choose another name to identify \
                              the store.")

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
        stores = self.get_all_art_stores()
        default = None

        if not stores:
            raise StoreError("Configure at least one store.")

        if len(stores) == 1:
            default = stores[0]
            default["is_default"] = True
            self._store_registry.register(default, DEFAULT_STORE)
            return

        for store in stores:
            if store.get("is_default", False):
                if default is None:
                    default = store
                    self._store_registry.register(default, DEFAULT_STORE)
                else:
                    raise StoreError("Configure only one store as default.")

        try:
            assert default["is_default"]
        except (AssertionError, TypeError):
            raise StoreError("Please configure one store as default.")

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

    def get_all_art_stores(self) -> List[dict]:
        """
        Get all artifact stores from registry.
        """
        return self._store_registry.get_all_stores(STORE_TYPE_ARTIFACT)

    def clean_all(self) -> None:
        """
        Clean up temp_dir contents.
        """
        self.clean_temp_path_store_cache()
        try:
            clean_all(self._tmp_dir)
        except FileNotFoundError:
            pass

    def clean_temp_path_store_cache(self) -> None:
        """
        Get rid of reference to temporary paths stored
        in artifact stores.
        """
        stores = self.get_all_art_stores()
        for store in stores:
            store["store"].clean_paths()
