"""
Factories module.
Contains registries of Stores and Runs and respective
factory methods.
"""
from __future__ import annotations

import typing
from typing import Optional, Tuple, Union

from datajudge.run import FrictionlessRun, GenericRun, RunInfo
from datajudge.store_artifact import LocalArtifactStore, S3ArtifactStore
from datajudge.store_metadata import LocalMetadataStore, RestMetadataStore
from datajudge.utils.constants import StoreType
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

DATA_STORE_REGISTRY = {
    "": LocalArtifactStore,
    "file": LocalArtifactStore,
    "s3": S3ArtifactStore,
}

RUN_REGISTRY = {
    "frictionless": FrictionlessRun,
    "generic": GenericRun
}


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
        if store_type == StoreType.METADATA.value:
            return METADATA_STORE_REGISTRY[scheme](new_uri, config)
        if store_type == StoreType.ARTIFACT.value:
            return ARTIFACT_STORE_REGISTRY[scheme](new_uri, config)
        if store_type == StoreType.DATA.value:
            return DATA_STORE_REGISTRY[scheme](new_uri, config, True)
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
