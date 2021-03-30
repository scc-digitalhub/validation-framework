from enum import Enum


class FileNames(Enum):
    """
    Enum for filenames, both metadata and artifact.
    """
    # Metadata
    RUN_METADATA = "run_metadata.json"
    DATA_RESOURCE = "data_resource.json"
    SHORT_REPORT = "report_short.json"
    ARTIFACT_METADATA = "artifact_metadata_{}.json"
    # Artifact
    FULL_REPORT = "report_full.json"
    SCHEMA_INFERRED = "inferred_schema.json"


class ApiEndpoint(Enum):
    """
    Enum API endpoints.
    """
    RUN_METADATA = "/run-metadata"
    DATA_RESOURCE = "/data-resource"
    SHORT_REPORT = "/report-short"
    ARTIFACT_METADATA = "/artifact-metadata"


class MetadataType(Enum):
    """
    Enum metadata types denomination.
    """
    RUN_METADATA = "run"
    DATA_RESOURCE = "resource"
    SHORT_REPORT = "report"
    ARTIFACT_METADATA = "artifact"
