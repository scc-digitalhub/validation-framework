"""
Factories module.
Contains registries of Stores and Runs and respective
factory methods.
"""
from __future__ import annotations

import typing
from typing import Union


from datajudge.store_artifact import (AzureArtifactStore, DummyArtifactStore,
                                      FTPArtifactStore, HTTPArtifactStore,
                                      LocalArtifactStore, S3ArtifactStore)
from datajudge.store_metadata import (DigitalHubMetadataStore,
                                      DummyMetadataStore, LocalMetadataStore)
from datajudge.utils import config as cfg
from datajudge.utils.config import StoreConfig
from datajudge.utils.file_utils import get_absolute_path
from datajudge.utils.uri_utils import check_url, get_uri_scheme, rebuild_uri

if typing.TYPE_CHECKING:
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
    "dummy": DummyMetadataStore,
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
    "dummy": DummyArtifactStore,
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
                 store_config: Union[dict, StoreConfig]
                 ) -> MetadataStore:
    """
    Function that returns metadata stores.
    """
    if store_config is None:
        return {"store": METADATA_STORE_REGISTRY["dummy"](None, None)}

    config = cfg_conversion(store_config)
    scheme = get_uri_scheme(config.uri)
    new_uri = resolve_uri_metadata(config.uri, scheme, project_name)
    try:
        return {"store": METADATA_STORE_REGISTRY[scheme](new_uri, config.config)}
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
               ) -> list:
    """
    Function that returns artifact stores.
    """

    stores = []

    if store_configs is None:
        stores.append({
            "name": "_dummy",
            "store": ARTIFACT_STORE_REGISTRY["dummy"](None, None),
            "is_default": True
            })
        return stores

    if not isinstance(store_configs, list):
        store_configs = [store_configs]

    for config in store_configs:
        config = cfg_conversion(config)
        scheme = get_uri_scheme(config.uri)
        new_uri = resolve_artifact_uri(config.uri, scheme)
        try:
            obj = ARTIFACT_STORE_REGISTRY[scheme](new_uri, config.config)
            stores.append({
                "name": config.name,
                "store": obj,
                "is_default": config.isDefault
            })
        except KeyError as k_err:
            raise KeyError from k_err

    return stores
