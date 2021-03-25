from __future__ import annotations

import typing
import urllib.parse
from typing import Optional, Tuple

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


def build_exp_metadata_uri(scheme: str,
                           uri: str,
                           experiment_id: str,
                           project_id: str) -> str:
    """
    Build experiment URI for metadata.
    """
    log_type = METADATA_LOG_TYPE
    if scheme in LOCAL_SCHEME:
        return get_absolute_path(uri, log_type, experiment_id)
    if scheme in REST_SCHEME:
        base_url = f"/api/project/{project_id}"
        return parse_url(uri + base_url)
    raise NotImplementedError


def build_exp_artifact_uri(scheme: str,
                           uri: str,
                           experiment_id: str) -> str:
    """
    Build experiment URI for artifact.
    """
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
    """
    Return a builded URI and it's scheme.
    """
    scheme = urllib.parse.urlparse(uri).scheme
    if store == "metadata":
        new_uri = build_exp_metadata_uri(scheme,
                                         uri,
                                         experiment_id,
                                         project_id)
    elif store == "artifact":
        new_uri = build_exp_artifact_uri(scheme,
                                         uri,
                                         experiment_id)
    else:
        raise RuntimeError("Invalid store.")
    return new_uri, scheme


def get_stores(project_id: str,
               experiment_id: str,
               metadata_store_uri: str,
               artifact_store_uri: str,
               metadata_creds: Optional[dict] = None,
               artifact_creds: Optional[dict] = None
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
                                           metadata_creds)
    store_artifact = select_artifact_store(scheme_artifact,
                                           uri_artifact,
                                           artifact_creds)

    return store_metadata, store_artifact


def select_metadata_store(scheme: str,
                          uri_metadata: str,
                          credentials: Optional[dict] = None
                          ) -> MetadataStore:
    """
    Factory method that returns a metadata store object to interact
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
    Factory method that returns an artifact store object to interact
    with various backends.
    """
    try:
        return ARTIFACT_STORE_REGISTRY[scheme](uri_artifact,
                                               credentials)
    except KeyError as k_err:
        raise NotImplementedError from k_err


def select_run_flavour(run_info_args: Tuple[str],
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
