"""
ArtifactStore registry.
"""
from datajudge.store_artifact.azure_artifact_store import AzureArtifactStore
from datajudge.store_artifact.dummy_artifact_store import DummyArtifactStore
from datajudge.store_artifact.ftp_artifact_store import FTPArtifactStore
from datajudge.store_artifact.http_artifact_store import HTTPArtifactStore
from datajudge.store_artifact.local_artifact_store import LocalArtifactStore
from datajudge.store_artifact.odbc_artifact_store import ODBCArtifactStore
from datajudge.store_artifact.s3_artifact_store import S3ArtifactStore
from datajudge.store_artifact.sql_artifact_store import SQLArtifactStore
from datajudge.utils.commons import (
    STORE_AZURE,
    STORE_DUMMY,
    STORE_FTP,
    STORE_HTTP,
    STORE_LOCAL,
    STORE_ODBC,
    STORE_S3,
    STORE_SQL,
)

ART_STORES = {
    STORE_AZURE: AzureArtifactStore,
    STORE_DUMMY: DummyArtifactStore,
    STORE_FTP: FTPArtifactStore,
    STORE_HTTP: HTTPArtifactStore,
    STORE_LOCAL: LocalArtifactStore,
    STORE_ODBC: ODBCArtifactStore,
    STORE_S3: S3ArtifactStore,
    STORE_SQL: SQLArtifactStore,
}
