from enum import Enum


class FileNames(Enum):
    """
    Enum for filenames, both metadata and artifact.
    """

    RUN_METADATA = "run_metadata.json"
    DATA_RESOURCE = "data_resource.json"
    SHORT_REPORT = "report_short.json"

    ARTIFACT_METADATA = "artifact_metadata.json"
    FULL_REPORT = "report_full.json"
    SCHEMA_INFERRED = "inferred_schema.json"


class ApiEndpoint(Enum):
    """
    Enum API endpoints.
    """

    RUN = "/run-metadata?overwrite={}"
    DATA_RESOURCE = "/data-resource"
    SHORT_REPORT = "/short-report"
    ARTIFACT = "/artifact-metadata"


class MetadataType(Enum):
    """
    Enum metadata types denomination.
    """

    RUN_METADATA = "run"
    SHORT_REPORT = "report"
    DATA_RESOURCE = "resource"
    ARTIFACT = "artifact"
    DATA_PACKAGE = "package"
