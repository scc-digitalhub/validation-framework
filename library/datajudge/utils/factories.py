"""
Factories module.
Contains registries of Stores and Runs and respective
factory methods.
"""
from __future__ import annotations

import typing
from typing import Optional, Tuple, Union

from datajudge.run import FrictionlessRun, GenericRun, RunInfo
from datajudge.store_artifact import (AzureArtifactStore, FTPArtifactStore,
                                      HTTPArtifactStore, LocalArtifactStore,
                                      S3ArtifactStore)
from datajudge.store_metadata import (DigitalHubMetadataStore,
                                      LocalMetadataStore)
from datajudge.utils import config as cfg
from datajudge.utils.file_utils import get_absolute_path
from datajudge.utils.uri_utils import check_url, get_uri_scheme, rebuild_uri

if typing.TYPE_CHECKING:
    from datajudge.client import Client
    from datajudge.data import DataResource
    from datajudge.run import Run
    from datajudge.store_artifact import ArtifactStore
    from datajudge.store_metadata import MetadataStore


# SCHEMES
LOCAL_SCHEME = ["", "file"]
HTTP_SCHEME = ["http", "https"]
S3_SCHEME = ["s3"]
AZURE_SCHEME = ["wasb", "wasbs"]
FTP_SCHEME = ["ftp"]


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

RUN_REGISTRY = {
    "frictionless": FrictionlessRun,
    "generic": GenericRun
}


def build_exp_uri(scheme: str,
                  uri: str,
                  experiment_id: str,
                  store: str,
                  project_id: Optional[str] = None) -> str:
    """
    Build experiment URI.
    """

    # Metadata stores
    if store == cfg.ST_METADATA:

        if scheme in LOCAL_SCHEME:
            return get_absolute_path(uri, store, experiment_id)

        if scheme in HTTP_SCHEME:
            if project_id is not None:
                url = uri + cfg.API_BASE + project_id
                return check_url(url)
            raise RuntimeError("'project_id' needed!")

        raise NotImplementedError

    # Artifact/data stores
    if store in (cfg.ST_DATA, cfg.ST_ARTIFACT):

        if scheme in LOCAL_SCHEME:
            return get_absolute_path(uri, store, experiment_id)
        if scheme in [*AZURE_SCHEME, *S3_SCHEME,
                      *HTTP_SCHEME, *FTP_SCHEME]:
            return rebuild_uri(uri, store, experiment_id)
        raise NotImplementedError

    raise RuntimeError("Invalid store.")


def resolve_uri(uri: str,
                experiment_id: str,
                store: str,
                project_id: Optional[str] = None) -> Tuple[str, str]:
    """
    Return a builded URI and it's scheme.
    """
    uri = uri if uri is not None else cfg.DEFAULT_LOCAL
    scheme = get_uri_scheme(uri)
    new_uri = build_exp_uri(scheme, uri, experiment_id, store, project_id)
    return new_uri, scheme


def get_store(store_type,
              project_id: str,
              experiment_id: str,
              uri: Optional[str] = None,
              config: Optional[dict] = None
              ) -> Union[MetadataStore, ArtifactStore]:
    """
    Function that returns metadata and artifact stores.
    """
    new_uri, scheme = resolve_uri(uri,
                                  experiment_id,
                                  store_type,
                                  project_id)
    try:
        if store_type == cfg.ST_METADATA:
            return METADATA_STORE_REGISTRY[scheme](new_uri, config)

        if store_type == cfg.ST_ARTIFACT:
            return ARTIFACT_STORE_REGISTRY[scheme](new_uri, config)

        if store_type == cfg.ST_DATA:
            return ARTIFACT_STORE_REGISTRY[scheme](new_uri, config, data=True)

        raise NotImplementedError

    except KeyError as k_err:
        raise KeyError from k_err


def get_run_flavour(run_info_args: Tuple[str],
                    library: str,
                    data_resource: DataResource,
                    client: Client,
                    overwrite: bool) -> Run:
    """
    Factory method that returns a run for a specific validation
    library.
    """
    try:
        run_info = RunInfo(*run_info_args)
        return RUN_REGISTRY[library](run_info,
                                     data_resource,
                                     client,
                                     overwrite)
    except KeyError as k_err:
        raise NotImplementedError from k_err
