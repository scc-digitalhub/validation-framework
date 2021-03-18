from __future__ import annotations

import typing
import urllib.parse
from typing import Any, Iterable, Optional, Tuple

from datajudge.run import FrictionlessRun, RunInfo
from datajudge.store_artifact import LocalArtifactStore, S3ArtifactStore
from datajudge.store_metadata import LocalMetadataStore, RestMetadataStore
from datajudge.utils.constants import OutputDesc
from datajudge.utils.file_utils import get_absolute_path
from datajudge.utils.s3_utils import build_s3_uri
from datajudge.utils.rest_utils import parse_url

if typing.TYPE_CHECKING:
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


LOCAL_SCHEME = ["", "file"]
REST_SCHEME = ["http", "https"]
S3_SCHEME = ["s3"]


def exp_uri_metadata(scheme: str,
                     uri: str,
                     experiment_id: str,
                     project_id: str) -> str:
    """Resolve experiment URI for metadata."""
    log_type = OutputDesc.METADATA.value
    if scheme in LOCAL_SCHEME:
        return get_absolute_path(uri, log_type, experiment_id)
    if scheme in REST_SCHEME:
        base_url = f"/api/p/{project_id}/e/{experiment_id}/"
        return parse_url(uri + base_url)
    raise NotImplementedError


def exp_uri_artifacts(scheme: str,
                      uri: str,
                      experiment_id: str) -> str:
    """Resolve experiment URI for artifacts."""
    log_type = OutputDesc.ARTIFACT.value
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
        new_uri = exp_uri_metadata(scheme, uri, experiment_id, project_id)
    elif store == "artifacts":
        new_uri = exp_uri_artifacts(scheme, uri, experiment_id)
    else:
        raise RuntimeError("Invalid store.")
    return new_uri, scheme


def get_stores(experiment_id: str,
               project_id: str,
               metadata_store_uri: str,
               artifacts_store_uri: str,
               credentials: Optional[dict] = None) -> Tuple[MetadataStore, ArtifactStore]:
        """Function that return metadata and artifact
        stores with authenticated credentials."""

        uri_metadata, scheme_metadata  = resolve_uri(metadata_store_uri,
                                                     experiment_id,
                                                     "metadata",
                                                     project_id)
        uri_artifacts, scheme_artifacts = resolve_uri(artifacts_store_uri,
                                                      experiment_id,
                                                      "artifacts")

        store_metadata = select_metadata_store(scheme_metadata, uri_metadata)
        store_artifacts = select_artifacts_store(scheme_artifacts, uri_artifacts, credentials)

        return store_metadata, store_artifacts


def select_metadata_store(scheme: str,
                          uri_metadata: str) -> MetadataStore:
    """
    Return a metadata store object to interact
    with various backends.
    """
    try:
        return METADATA_STORE_REGISTRY[scheme](uri_metadata)
    except KeyError:
        raise NotImplementedError


def select_artifacts_store(scheme: str,
                           uri_artifacts: str,
                           credentials: Optional[dict] = None) -> ArtifactStore:
    """
    Return an artifact store object to interact
    with various backends.
    """
    try:
        return ARTIFACT_STORE_REGISTRY[scheme](uri_artifacts,
                                               credentials)
    except KeyError:
        raise NotImplementedError


def select_run_flavour(run_info_args: Iterable[str],
                       library: str,
                       data_resource: Any,
                       client: Any) -> Run:
    """
    Return a run for a specific validation
    library.
    """
    try:
        run_info = RunInfo(*run_info_args)
        return  RUN_REGISTRY[library](run_info,
                                      data_resource,
                                      client)
    except KeyError:
        raise NotImplementedError
