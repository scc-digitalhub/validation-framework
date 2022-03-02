"""
Factories module.
Contains registries of Stores and Runs and respective
factory methods.
"""
from __future__ import annotations

import typing
from typing import Tuple, Union

from datajudge.run import Run, RunInfo, PluginHandler
from datajudge.run.plugin import (InferencePluginDummy,
                                  InferencePluginFrictionless,
                                  ProfilePluginDummy,
                                  ProfilePluginFrictionless,
                                  ProfilePluginPandasProfiling,
                                  ValidationPluginDummy,
                                  ValidationPluginFrictionless)
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
    from datajudge.client import Client
    from datajudge.store_artifact import ArtifactStore
    from datajudge.store_metadata import MetadataStore
    from datajudge.utils.config import RunConfig


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

PLUGIN_REGISTRY = {
    "inference": {
        "dummy": InferencePluginDummy,
        "frictionless": InferencePluginFrictionless,
        },
    "validation": {
        "dummy": ValidationPluginDummy,
        "frictionless": ValidationPluginFrictionless,
        },
    "profiling": {
        "dummy": ProfilePluginDummy,
        "frictionless": ProfilePluginFrictionless,
        "pandas_profiling": ProfilePluginPandasProfiling,
        },
    "snapshot": {
    }
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
        return METADATA_STORE_REGISTRY["dummy"](None, None)

    config = cfg_conversion(store_config)
    scheme = get_uri_scheme(config.path)
    new_uri = resolve_uri_metadata(config.path, scheme, project_name)
    try:
        return METADATA_STORE_REGISTRY[scheme](new_uri, config.config)
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
    if store_configs is None:
        return {
            "_dummy": {
                "store": ARTIFACT_STORE_REGISTRY["dummy"](None, None),
                "is_default": True
            }
        }

    if not isinstance(store_configs, list):
        store_configs = [store_configs]
    stores = {}
    for config in store_configs:
        config = cfg_conversion(config)
        scheme = get_uri_scheme(config.path)
        new_uri = resolve_artifact_uri(config.path, scheme)
        try:
            obj = ARTIFACT_STORE_REGISTRY[scheme](new_uri, config.config)
            stores[config.name] = {
                "store": obj,
                "is_default": config.isDefault
            }
        except KeyError as k_err:
            raise KeyError from k_err

    return stores


def get_plugin(config: dict,
               typology: str) -> list:
    """
    Factory method that creates run plugins.
    """
    plugin_list = {}
    if config is None:
        plugin_list["dummy"] = PLUGIN_REGISTRY[typology]["dummy"]()
        return plugin_list
    if config.enabled:
        if not isinstance(config.library, list):
            config.library = [config.library]
        for lib in config.library:
            try:
                plugin_list[lib] = PLUGIN_REGISTRY[typology][lib]()
            except KeyError as k_err:
                raise NotImplementedError from k_err
        return plugin_list
    plugin_list["dummy"] = PLUGIN_REGISTRY[typology]["dummy"]()
    return plugin_list


def get_plugin_handler(run_config: RunConfig) -> PluginHandler:
    """
    Build a plugin handler for the run.
    """
    inference = get_plugin(run_config.inference, "inference")
    validation = get_plugin(run_config.validation, "validation")
    profiling = get_plugin(run_config.profiling, "profiling")
    return PluginHandler(inference,
                         validation,
                         profiling)


def get_run(run_info_args: Tuple[str],
            run_plugin_handler: PluginHandler,
            client: Client,
            overwrite: bool) -> Run:
    """
    Factory method that returns a run.
    """
    try:
        run_info = RunInfo(*run_info_args)
        return Run(run_info,
                   run_plugin_handler,
                   client,
                   overwrite)
    except Exception as ex:
        raise ex
