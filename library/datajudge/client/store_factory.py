"""
StoreFactory module.
"""
from __future__ import annotations

import typing
from pathlib import Path
from typing import Union

from datajudge.store_artifact.registry import ART_STORES
from datajudge.store_metadata.registry import MD_STORES
from datajudge.utils.commons import (API_BASE, GENERIC_DUMMY, SCHEME_AZURE,
                                     SCHEME_DUMMY, SCHEME_FTP, SCHEME_HTTP,
                                     SCHEME_LOCAL, SCHEME_ODBC, SCHEME_S3,
                                     SCHEME_SQL, STORE_DUMMY)
from datajudge.utils.config import StoreConfig
from datajudge.utils.file_utils import get_absolute_path
from datajudge.utils.uri_utils import (check_url, get_uri_netloc, get_uri_path,
                                       get_uri_scheme, rebuild_uri)
from datajudge.utils.utils import get_uiid

if typing.TYPE_CHECKING:
    from datajudge.store_artifact.artifact_store import ArtifactStore
    from datajudge.store_metadata.metadata_store import MetadataStore


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

    def build_metadata_store(self,
                             cfg: StoreConfig) -> MetadataStore:
        """
        Method to create a metadata stores.
        """
        scheme = get_uri_scheme(cfg.uri)
        new_uri = self.resolve_uri_metadata(cfg.uri,
                                            scheme,
                                            self.project_id)
        try:
            return MD_STORES[cfg.type](cfg.name, new_uri, cfg.config)
        except KeyError:
            raise NotImplementedError

    @staticmethod
    def resolve_uri_metadata(uri: str,
                             scheme: str,
                             project_name: str) -> str:
        """
        Resolve metadata URI location.
        """
        if scheme in [*SCHEME_LOCAL]:
            return get_absolute_path(get_uri_netloc(uri),
                                     get_uri_path(uri),
                                     "metadata")
        if scheme in [*SCHEME_HTTP]:
            url = uri + API_BASE + project_name
            return check_url(url)
        if scheme in [*SCHEME_DUMMY]:
            return uri
        raise NotImplementedError

    def build_artifact_store(self,
                             cfg: StoreConfig) -> ArtifactStore:
        """
        Method to create a artifact stores.
        """
        scheme = get_uri_scheme(cfg.uri)
        new_uri = self.resolve_artifact_uri(cfg.uri, scheme)
        tmp = str(Path(self.tmp_dir, get_uiid()))
        try:
            return ART_STORES[cfg.type](cfg.name,
                                        new_uri,
                                        tmp,
                                        cfg.config,
                                        cfg.isDefault)
        except KeyError:
            raise NotImplementedError

    @staticmethod
    def resolve_artifact_uri(uri: str, scheme: str) -> str:
        """
        Resolve artifact URI location.
        """
        if scheme in [*SCHEME_LOCAL]:
            return get_absolute_path(get_uri_netloc(uri),
                                     get_uri_path(uri),
                                     "artifact")
        if scheme in [*SCHEME_AZURE, *SCHEME_S3, *SCHEME_FTP]:
            return rebuild_uri(uri, "artifact")
        if scheme in [*SCHEME_DUMMY, *SCHEME_HTTP,
                      *SCHEME_SQL, *SCHEME_ODBC]:
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
            return StoreConfig(name=GENERIC_DUMMY,
                               type=STORE_DUMMY,
                               uri=f"{SCHEME_DUMMY}://")
        if not isinstance(config, StoreConfig):
            try:
                return StoreConfig(**config)
            except TypeError:
                raise TypeError("Malformed store configuration.")
        return config
