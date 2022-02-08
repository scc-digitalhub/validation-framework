"""
Factories module.
Contains registries of Stores and Runs and respective
factory methods.
"""
from __future__ import annotations

import typing
from typing import Any, List, Optional, Tuple, Union

from datajudge.run import RunInfo, Run
from datajudge.store_artifact import (AzureArtifactStore, FTPArtifactStore,
                                      HTTPArtifactStore, LocalArtifactStore,
                                      S3ArtifactStore)
from datajudge.store_metadata import (DigitalHubMetadataStore,
                                      LocalMetadataStore)
from datajudge.utils import config as cfg
from datajudge.utils.config import StoreConfig
from datajudge.utils.file_utils import get_absolute_path
from datajudge.utils.uri_utils import check_url, get_uri_scheme, rebuild_uri

if typing.TYPE_CHECKING:
    from datajudge.client import Client
    from datajudge.data import DataResource
    from datajudge.store_artifact import ArtifactStore
    from datajudge.store_metadata import MetadataStore


META = cfg.ST_METADATA
DATA = cfg.ST_ARTIFACT

# Schemes
LOCAL_SCHEME = ["", "file"]
HTTP_SCHEME = ["http", "https"]
S3_SCHEME = ["s3"]
AZURE_SCHEME = ["wasb", "wasbs"]
FTP_SCHEME = ["ftp"]

# Registries
METADATA_STORE_REGISTRY = {
    "": LocalMetadataStore,
    "file": LocalMetadataStore,
    "http": DigitalHubMetadataStore,
    "https": DigitalHubMetadataStore,
}

ARTIFACT_STORE_REGISTRY = {
    "": LocalArtifactStore,
    "file": LocalArtifactStore,
    "s3": S3ArtifactStore,
    "wasb": AzureArtifactStore,
    "wasbs": AzureArtifactStore,
    "http": HTTPArtifactStore,
    "https": HTTPArtifactStore,
    "ftp": FTPArtifactStore,
}


def build_exp_uri(scheme: str,
                  uri: str,
                  experiment_name: str,
                  store: str,
                  project_id: Optional[str] = None) -> str:
    """
    Build experiment URI.
    """

    # Metadata stores
    if store == META:

        if scheme in LOCAL_SCHEME:
            return get_absolute_path(uri, store, experiment_name)

        if scheme in HTTP_SCHEME:
            if project_id is not None:
                url = uri + cfg.API_BASE + project_id
                return check_url(url)
            raise RuntimeError("'project_id' needed!")

        raise NotImplementedError

    # Artifact/data stores
    if store == DATA:

        if scheme in LOCAL_SCHEME:
            return get_absolute_path(uri, store, experiment_name)
        if scheme in [*AZURE_SCHEME, *S3_SCHEME, *HTTP_SCHEME, *FTP_SCHEME]:
            return rebuild_uri(uri, store, experiment_name)
        raise NotImplementedError

    raise RuntimeError("Invalid store.")


def resolve_uri(uri: str,
                experiment_name: str,
                store: str,
                project_id: Optional[str] = None) -> Tuple[str, str]:
    """
    Return a builded URI and it's scheme.
    """
    scheme = get_uri_scheme(uri)
    new_uri = build_exp_uri(scheme, uri, experiment_name, store, project_id)
    return new_uri, scheme


def cfg_conversion(config: Union[StoreConfig, dict]) -> StoreConfig:
    """
    Try to convert a store configuration in a StoreConfig model.
    """    
    if not isinstance(config, StoreConfig):
        try:
            return StoreConfig(**config)
        except Exception as ex:
            raise ex
    return config


def get_md_store(project_id: str,
                 experiment_name: str,
                 config: Union[dict, StoreConfig]
                 ) -> MetadataStore:
    """
    Function that returns metadata stores.
    """
    config = cfg_conversion(config)
    uri = config.path
    new_uri, scheme = resolve_uri(uri,
                                  experiment_name,
                                  META,
                                  project_id)
    try:
        return METADATA_STORE_REGISTRY[scheme](new_uri, config)
    except KeyError as k_err:
        raise KeyError from k_err

def get_stores(experiment_name: str,
               store_configs: Union[dict, StoreConfig, list]
               ) -> ArtifactStore:
    """
    Function that returns artifact stores.
    """
    if not isinstance(store_configs, list):
        store_configs = [store_configs]

    stores = {}
    for cfg in store_configs:
        cfg = cfg_conversion(cfg)
        new_uri, scheme = resolve_uri(cfg.path,
                                      experiment_name,
                                      DATA)
        try:
            obj = ARTIFACT_STORE_REGISTRY[scheme](new_uri, cfg.config)
            stores[cfg.name] = {
                "store": obj,
                "is_default": cfg.isDefault 
            }
        except KeyError as k_err:
            raise KeyError from k_err
    
    print(stores)
    
    return stores


def get_run(run_info_args: Tuple[str],
            data_resource: DataResource,
            client: Client,
            overwrite: bool) -> Run:
    """
    Factory method that returns a run.
    """
    try:
        run_info = RunInfo(*run_info_args)
        return Run(run_info,
                   data_resource,
                   client,
                   overwrite)

    except KeyError as k_err:
        raise NotImplementedError from k_err
