from enum import Enum


class FileNames(Enum):
    """
    Enum for filenames, both metadata and artifact.
    """
    # Metadata
    RUN_METADATA = "run_metadata.json"
    DATA_RESOURCE = "data_resource.json"
    SHORT_REPORT = "report_short.json"
    SHORT_SCHEMA = "schema_short.json"
    DATA_PROFILE = "data_profile.json"
    ARTIFACT_METADATA = "artifact_metadata_{}.json"
    # Artifact
    FULL_REPORT = "report_full.json"
    SCHEMA_INFERRED = "inferred_schema.json"
    FULL_PROFILE = "pandas_profile.json"


class ApiEndpoint(Enum):
    """
    Enum API endpoints.
    """
    RUN_METADATA = "/run-metadata"
    DATA_RESOURCE = "/data-resource"
    SHORT_REPORT = "/report-short"
    SHORT_SCHEMA = "/schema-short"
    DATA_PROFILE = "/data-profile"
    ARTIFACT_METADATA = "/artifact-metadata"


class MetadataType(Enum):
    """
    Enum metadata types denomination.
    """
    RUN_METADATA = "run"
    DATA_RESOURCE = "resource"
    SHORT_REPORT = "report"
    SHORT_SCHEMA = "schema"
    DATA_PROFILE = "profile"
    ARTIFACT_METADATA = "artifact"


class StoreType(Enum):
    """
    Enum Store types.
    """
    METADATA = "metadata"
    ARTIFACT = "artifact"
    DATA = "data"
