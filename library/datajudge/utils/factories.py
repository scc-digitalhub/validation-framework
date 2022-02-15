"""
Factories module.
Contains registries of Stores and Runs and respective
factory methods.
"""
from __future__ import annotations

import typing
from typing import Optional, Tuple, Union

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


def resolve_uri_metadata(uri: str,
                         scheme: str,
                         project_name: str) -> str:
    """
    Build metadata URI store to be formatted by client.
    """
    if scheme in LOCAL_SCHEME:
        return get_absolute_path(uri, "metadata")
    if scheme in HTTP_SCHEME:
        url = uri + cfg.API_BASE + project_name
        return check_url(url)
    raise NotImplementedError


def get_md_store(project_name: str,
                 config: Union[dict, StoreConfig]
                 ) -> MetadataStore:
    """
    Function that returns metadata stores.
    """
    cfg = cfg_conversion(config)
    scheme = get_uri_scheme(cfg.path)
    new_uri = resolve_uri_metadata(cfg.path, scheme, project_name)
    try:
        return METADATA_STORE_REGISTRY[scheme](new_uri, cfg.config)
    except KeyError as k_err:
        raise KeyError from k_err


def resolve_artifact_uri(uri: str, scheme: str) -> str:
    """
    Build artifact URI store to be formatted by client.
    """
    if scheme in LOCAL_SCHEME:
        return get_absolute_path(uri, "artifact")
    if scheme in [*AZURE_SCHEME, *S3_SCHEME, *HTTP_SCHEME, *FTP_SCHEME]:
        return rebuild_uri(uri, "artifact")
    raise NotImplementedError


def get_stores(store_configs: Union[dict, StoreConfig, list]
               ) -> ArtifactStore:
    """
    Function that returns artifact stores.
    """
    if not isinstance(store_configs, list):
        store_configs = [store_configs]

    stores = {}
    for cfg in store_configs:
        cfg = cfg_conversion(cfg)
        scheme = get_uri_scheme(cfg.path)
        new_uri = resolve_artifact_uri(cfg.path, scheme)
        try:
            obj = ARTIFACT_STORE_REGISTRY[scheme](new_uri, cfg.config)
            stores[cfg.name] = {
                "store": obj,
                "is_default": cfg.isDefault 
            }
        except KeyError as k_err:
            raise KeyError from k_err
    
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
