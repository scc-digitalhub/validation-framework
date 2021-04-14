from __future__ import annotations

import typing
from typing import Optional, Tuple

from datajudge.run import FrictionlessRun, RunInfo
from datajudge.store_artifact import LocalArtifactStore, S3ArtifactStore
from datajudge.store_metadata import LocalMetadataStore, RestMetadataStore
from datajudge.utils.uri_utils import resolve_uri

if typing.TYPE_CHECKING:
    from datajudge.client import Client
    from datajudge.data import DataResource
    from datajudge.run import Run
    from datajudge.store_artifact import ArtifactStore
    from datajudge.store_metadata import MetadataStore


METADATA_STORE_REGISTRY = {
    "": LocalMetadataStore,
    "file": LocalMetadataStore,
    "http": RestMetadataStore,
    "https": RestMetadataStore
}

ARTIFACT_STORE_REGISTRY = {
    "": LocalArtifactStore,
    "file": LocalArtifactStore,
    "s3": S3ArtifactStore,
}

RUN_REGISTRY = {
    "frictionless": FrictionlessRun
}


def get_stores(project_id: str,
               experiment_id: str,
               metadata_store_uri: str,
               artifact_store_uri: str,
               metadata_config: Optional[dict] = None,
               artifact_config: Optional[dict] = None
               ) -> Tuple[MetadataStore, ArtifactStore]:
    """
    Function that returns metadata and artifact stores.
    """
    uri_metadata, scheme_metadata = resolve_uri(metadata_store_uri,
                                                experiment_id,
                                                "metadata",
                                                project_id)
    uri_artifact, scheme_artifact = resolve_uri(artifact_store_uri,
                                                experiment_id,
                                                "artifact")

    store_metadata = select_metadata_store(scheme_metadata,
                                           uri_metadata,
                                           metadata_config)
    store_artifact = select_artifact_store(scheme_artifact,
                                           uri_artifact,
                                           artifact_config)

    return store_metadata, store_artifact


def select_metadata_store(scheme: str,
                          uri_metadata: str,
                          config: Optional[dict] = None
                          ) -> MetadataStore:
    """
    Factory method that returns a metadata store object to interact
    with various backends.
    """
    try:
        return METADATA_STORE_REGISTRY[scheme](uri_metadata,
                                               config)
    except KeyError as k_err:
        raise NotImplementedError from k_err


def select_artifact_store(scheme: str,
                          uri_artifact: str,
                          config: Optional[dict] = None
                          ) -> ArtifactStore:
    """
    Factory method that returns an artifact store object to interact
    with various backends.
    """
    try:
        return ARTIFACT_STORE_REGISTRY[scheme](uri_artifact,
                                               config)
    except KeyError as k_err:
        raise NotImplementedError from k_err


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
