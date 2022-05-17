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
from datajudge.utils.commons import (API_BASE, AZURE, AZURE_SCHEME, DUMMY,
                                     DUMMY_SCHEME, FTP, FTP_SCHEME, HTTP,
                                     HTTP_SCHEME, LOCAL, LOCAL_SCHEME, ODBC,
                                     ODBC_SCHEME, S3, S3_SCHEME, SQL,
                                     SQL_SCHEME)
from datajudge.utils.config import DUMMY_STORE, StoreConfig
from datajudge.utils.file_utils import get_absolute_path
from datajudge.utils.uri_utils import check_url, get_uri_scheme, rebuild_uri
from datajudge.utils.utils import get_uiid

# Registries

MD_STORES = {
    LOCAL: LocalMetadataStore,
    HTTP: DigitalHubMetadataStore,
    DUMMY: DummyMetadataStore,
}

ART_STORES = {
    LOCAL: LocalArtifactStore,
    HTTP: HTTPArtifactStore,
    S3: S3ArtifactStore,
    AZURE: AzureArtifactStore,
    FTP: FTPArtifactStore,
    SQL: SQLArtifactStore,
    ODBC: ODBCArtifactStore,
    DUMMY: DummyArtifactStore,
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
        cfg = self._check_config(config)
        if md_store:
            return self.build_metadata_store(cfg)
        return self.build_artifact_store(cfg)

    def build_metadata_store(self, cfg: StoreConfig) -> dict:
        """
        Method to create a metadata stores.
        """
        scheme = get_uri_scheme(cfg.uri)
        new_uri = self.resolve_uri_metadata(cfg.uri,
                                            scheme,
                                            self.project_id)
        try:
            return {
                "name": cfg.name,
                "store": MD_STORES[cfg.type](cfg.name, new_uri, cfg.config)
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

    def build_artifact_store(self, cfg: StoreConfig) -> dict:
        """
        Method to create a artifact stores.
        """
        scheme = get_uri_scheme(cfg.uri)
        new_uri = self.resolve_artifact_uri(cfg.uri, scheme)
        tmp = str(Path(self.tmp_dir, get_uiid()))
        try:
            return {
                "name": cfg.name,
                "store": ART_STORES[cfg.type](cfg.name, new_uri, tmp, cfg.config),
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
    def _check_config(config: Union[StoreConfig, dict]) -> StoreConfig:
        """
        Try to convert a dictionary in a StoreConfig model.
        In case the config parameter is None, return a dummy store basic
        config.
        """
        if config is None:
            return DUMMY_STORE
        if not isinstance(config, StoreConfig):
            try:
                return StoreConfig(**config)
            except TypeError:
                raise TypeError("Malformed store configuration.")
        return config
