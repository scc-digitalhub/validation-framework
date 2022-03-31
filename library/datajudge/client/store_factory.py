"""
Factories module.
Contains registries of Stores and Runs and respective
factory methods.
"""
# pylint: disable=raise-missing-from
from typing import Union

from datajudge.store_artifact import (AzureArtifactStore, DummyArtifactStore,
                                      FTPArtifactStore, HTTPArtifactStore,
                                      LocalArtifactStore, S3ArtifactStore)
from datajudge.store_artifact.dremio_artifact_store import DremioArtifactStore
from datajudge.store_artifact.sql_artifact_store import SQLArtifactStore
from datajudge.store_metadata import (DigitalHubMetadataStore,
                                      DummyMetadataStore, LocalMetadataStore)
from datajudge.utils.commons import API_BASE
from datajudge.utils.config import StoreConfig
from datajudge.utils.file_utils import get_absolute_path
from datajudge.utils.uri_utils import check_url, get_uri_scheme, rebuild_uri

# Schemes

LOCAL_SCHEME = ["", "file"]
HTTP_SCHEME = ["http", "https"]
S3_SCHEME = ["s3"]
AZURE_SCHEME = ["wasb", "wasbs"]
FTP_SCHEME = ["ftp"]
SQL_SCHEME = ["sql"]
DREMIO_SCHEME = ["dremio"]
DUMMY_SCHEME = ["dummy"]

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
    "sql": SQLArtifactStore,
    "dremio": DremioArtifactStore,
    "dummy": DummyArtifactStore,
}


class StoreBuilder:
    """
    StoreBuilder class.

    In the library workflow, it's associated with
    a client and a project. It builds stores for a
    specific client.

    """

    def __init__(self, project_id: str) -> None:
        self.project_id = project_id

    def build(self,
              config: Union[dict, StoreConfig],
              md_store: bool = False) -> dict:
        """
        Generic build method.
        """
        cfg = self.cfg_conversion(config)
        scheme = get_uri_scheme(cfg.uri)
        if md_store:
            return self.build_metadata_store(cfg, scheme)
        return self.build_artifact_store(cfg, scheme)

    def build_metadata_store(self, cfg: StoreConfig, scheme: str) -> dict:
        """
        Function that returns metadata stores.
        """
        new_uri = self.resolve_uri_metadata(cfg.uri,
                                            scheme,
                                            self.project_id)
        try:
            return {
                "name": cfg.name,
                "store": METADATA_STORE_REGISTRY[scheme](new_uri,
                                                         cfg.config)
            }
        except KeyError:
            raise NotImplementedError

    @staticmethod
    def resolve_uri_metadata(uri: str,
                             scheme: str,
                             project_name: str) -> str:
        """
        Build metadata URI store to be formatted by client.
        """
        if scheme in [*LOCAL_SCHEME]:
            return get_absolute_path(uri, "metadata")
        if scheme in [*HTTP_SCHEME]:
            url = uri + API_BASE + project_name
            return check_url(url)
        if scheme in [*DUMMY_SCHEME]:
            return uri
        raise NotImplementedError

    def build_artifact_store(self, cfg: StoreConfig, scheme: str) -> dict:
        """
        Function that returns artifact stores.
        """
        new_uri = self.resolve_artifact_uri(cfg.uri, scheme)
        try:
            return {
                "name": cfg.name,
                "store": ARTIFACT_STORE_REGISTRY[scheme](new_uri, cfg.config),
                "is_default": cfg.isDefault
            }
        except KeyError:
            raise NotImplementedError

    @staticmethod
    def resolve_artifact_uri(uri: str, scheme: str) -> str:
        """
        Build artifact URI store to be formatted by client.
        """
        if scheme in [*LOCAL_SCHEME]:
            return get_absolute_path(uri, "artifact")
        if scheme in [*AZURE_SCHEME, *S3_SCHEME,
                      *HTTP_SCHEME, *FTP_SCHEME,
                      *SQL_SCHEME, *DREMIO_SCHEME]:
            return rebuild_uri(uri, "artifact")
        if scheme in [*DUMMY_SCHEME]:
            return uri
        raise NotImplementedError

    @staticmethod
    def cfg_conversion(config: Union[StoreConfig, dict]) -> StoreConfig:
        """
        Try to convert a store configuration in a StoreConfig model.
        """
        if not isinstance(config, StoreConfig):
            if config is None:
                return StoreConfig(name="_dummy",
                                   uri="dummy://",
                                   isDefault=True)
            try:
                return StoreConfig(**config)
            except TypeError:
                raise RuntimeError("Malformed store configuration.")
        return config
