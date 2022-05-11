"""
StoreFactory module.
"""
# pylint: disable=raise-missing-from
from pathlib import Path
from typing import Union

from datajudge.store_artifact import (AzureArtifactStore, DummyArtifactStore,
                                      FTPArtifactStore, HTTPArtifactStore,
                                      LocalArtifactStore, S3ArtifactStore)
from datajudge.store_artifact.odbc_artifact_store import ODBCArtifactStore
from datajudge.store_artifact.sql_artifact_store import SQLArtifactStore
from datajudge.store_metadata import (DigitalHubMetadataStore,
                                      DummyMetadataStore, LocalMetadataStore)
from datajudge.utils.commons import API_BASE
from datajudge.utils.config import StoreConfig
from datajudge.utils.file_utils import get_absolute_path
from datajudge.utils.uri_utils import check_url, get_uri_scheme, rebuild_uri
from datajudge.utils.utils import get_uiid

# Schemes

LOCAL_SCHEME = ["", "file"]
HTTP_SCHEME = ["http", "https"]
S3_SCHEME = ["s3"]
AZURE_SCHEME = ["wasb", "wasbs"]
FTP_SCHEME = ["ftp"]
SQL_SCHEME = ["sql"]
ODBC_SCHEME = ["dremio"]
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
    "dremio": ODBCArtifactStore,
    "dummy": DummyArtifactStore,
}


class StoreBuilder:
    """
    StoreBuilder class.
    """

    def __init__(self,
                 project_id: str,
                 tmp_dir: str) -> None:
        self.project_id = project_id
        self.tmp_dir = tmp_dir

    def build(self,
              config: Union[dict, StoreConfig],
              md_store: bool = False) -> dict:
        """
        Builder method that recieves store configurations.
        """
        cfg = self.cfg_conversion(config)
        scheme = get_uri_scheme(cfg.uri)
        if md_store:
            return self.build_metadata_store(cfg, scheme)
        return self.build_artifact_store(cfg, scheme)

    def build_metadata_store(self, cfg: StoreConfig, scheme: str) -> dict:
        """
        Method to create a metadata stores.
        """
        new_uri = self.resolve_uri_metadata(cfg.uri,
                                            scheme,
                                            self.project_id)
        try:
            return {
                "name": cfg.name,
                "store": METADATA_STORE_REGISTRY[scheme](cfg.name,
                                                         new_uri,
                                                         cfg.config)
            }
        except KeyError:
            raise NotImplementedError

    @staticmethod
    def resolve_uri_metadata(uri: str,
                             scheme: str,
                             project_name: str) -> str:
        """
        Resolve metadata URI location.
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
        Method to create a artifact stores.
        """
        new_uri = self.resolve_artifact_uri(cfg.uri, scheme)
        temp_partition = str(Path(self.tmp_dir, get_uiid()))
        try:
            return {
                "name": cfg.name,
                "store": ARTIFACT_STORE_REGISTRY[scheme](cfg.name,
                                                         new_uri,
                                                         temp_partition,
                                                         cfg.config),
                "is_default": cfg.isDefault
            }
        except KeyError:
            raise NotImplementedError

    @staticmethod
    def resolve_artifact_uri(uri: str, scheme: str) -> str:
        """
        Resolve artifact URI location.
        """
        if scheme in [*LOCAL_SCHEME]:
            return get_absolute_path(uri, "artifact")
        if scheme in [*AZURE_SCHEME, *S3_SCHEME,
                      *HTTP_SCHEME, *FTP_SCHEME,
                      *SQL_SCHEME, *ODBC_SCHEME]:
            return rebuild_uri(uri, "artifact")
        if scheme in [*DUMMY_SCHEME]:
            return uri
        raise NotImplementedError

    @staticmethod
    def cfg_conversion(config: Union[StoreConfig, dict]) -> StoreConfig:
        """
        Try to convert a dictionary in a StoreConfig model.
        In case the config parameter is None, return a dummy store basic
        config.
        """
        if config is None:
            return StoreConfig(name="_dummy",
                               uri="dummy://",
                               isDefault=True)
        if not isinstance(config, StoreConfig):
            try:
                return StoreConfig(**config)
            except TypeError:
                raise TypeError("Malformed store configuration.")
        return config
