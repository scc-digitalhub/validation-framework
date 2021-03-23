from __future__ import annotations

import typing
import urllib.parse
from typing import Iterable, Optional, Tuple

from datajudge.run import FrictionlessRun, RunInfo
from datajudge.store_artifact import LocalArtifactStore, S3ArtifactStore
from datajudge.store_metadata import LocalMetadataStore, RestMetadataStore
from datajudge.utils.file_utils import get_absolute_path
from datajudge.utils.s3_utils import build_s3_uri
from datajudge.utils.rest_utils import parse_url

if typing.TYPE_CHECKING:
    from datajudge.client import Client
    from datajudge.data import DataResource
    from datajudge.run import Run
    from datajudge.store_artifact import ArtifactStore
    from datajudge.store_metadata import MetadataStore


METADATA_LOG_TYPE = "metadata"
ARTIFACT_LOG_TYPE = "artifact"

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

LOCAL_SCHEME = ["", "file"]
REST_SCHEME = ["http", "https"]
S3_SCHEME = ["s3"]


def resolve_uri_metadata(scheme: str,
                         uri: str,
                         experiment_id: str,
                         project_id: str) -> str:
    """Resolve experiment URI for metadata."""
    log_type = METADATA_LOG_TYPE
    if scheme in LOCAL_SCHEME:
        return get_absolute_path(uri, log_type, experiment_id)
    if scheme in REST_SCHEME:
        base_url = f"/api/p/{project_id}/e/{experiment_id}/"
        return parse_url(uri + base_url)
    raise NotImplementedError


def resolve_uri_artifact(scheme: str,
                         uri: str,
                         experiment_id: str) -> str:
    """Resolve experiment URI for artifact."""
    log_type = ARTIFACT_LOG_TYPE
    if scheme in LOCAL_SCHEME:
        return get_absolute_path(uri, log_type, experiment_id)
    if scheme in S3_SCHEME:
        return build_s3_uri(uri, log_type, experiment_id)
    raise NotImplementedError


def resolve_uri(uri: str,
                experiment_id: str,
                store: str,
                project_id: Optional[str] = None) -> Tuple[str, str]:
    """Return a builded URI for the
    artifact/metadata store and it's schema."""
    scheme = urllib.parse.urlparse(uri).scheme
    if store == "metadata":
        new_uri = resolve_uri_metadata(scheme, uri, experiment_id, project_id)
    elif store == "artifact":
        new_uri = resolve_uri_artifact(scheme, uri, experiment_id)
    else:
        raise RuntimeError("Invalid store.")
    return new_uri, scheme


def get_stores(experiment_id: str,
               project_id: str,
               metadata_params: dict,
               artifact_params: dict
               ) -> Tuple[MetadataStore, ArtifactStore]:
    """Function that return metadata and artifact
    stores with authenticated credentials."""

    metadata_store_uri, metadata_creds = metadata_params.values()
    artifact_store_uri, artifact_creds = artifact_params.values()


    uri_metadata, scheme_metadata = resolve_uri(metadata_store_uri,
                                                experiment_id,
                                                "metadata",
                                                project_id)
    uri_artifact, scheme_artifact = resolve_uri(artifact_store_uri,
                                                experiment_id,
                                                "artifact")

    store_metadata = select_metadata_store(scheme_metadata, uri_metadata, metadata_creds)
    store_artifact = select_artifact_store(scheme_artifact, uri_artifact, artifact_creds)

    return store_metadata, store_artifact


def select_metadata_store(scheme: str,
                          uri_metadata: str,
                          credentials: Optional[dict] = None
                          ) -> MetadataStore:
    """
    Return a metadata store object to interact
    with various backends.
    """
    try:
        return METADATA_STORE_REGISTRY[scheme](uri_metadata,
                                               credentials)
    except KeyError as k_err:
        raise NotImplementedError from k_err


def select_artifact_store(scheme: str,
                          uri_artifact: str,
                          credentials: Optional[dict] = None
                          ) -> ArtifactStore:
    """
    Return an artifact store object to interact
    with various backends.
    """
    try:
        return ARTIFACT_STORE_REGISTRY[scheme](uri_artifact,
                                               credentials)
    except KeyError as k_err:
        raise NotImplementedError from k_err


def select_run_flavour(run_info_args: Iterable[str],
                       library: str,
                       data_resource: DataResource,
                       client: Client) -> Run:
    """
    Return a run for a specific validation
    library.
    """
    try:
        run_info = RunInfo(*run_info_args)
        return RUN_REGISTRY[library](run_info,
                                     data_resource,
                                     client)
    except KeyError as k_err:
        raise NotImplementedError from k_err
