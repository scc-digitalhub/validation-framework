from enum import Enum


# Default names
EXP_NAME = "DefaultExp"
PROJ_ID = "DefaultProj"
METADATA_STORE_PARAMS = {
    "store_uri" : "./validruns",
    "credentials": None
}
ARTIFACT_STORE_PARAMS = {
    "store_uri" : "./validruns",
    "credentials": None
}


class FileNames(Enum):
    """
    Enum for filenames, both metadata and artifact.
    """

    RUN_METADATA = "run_metadata.json"
    DATA_RESOURCE = "data_resource.json"
    SHORT_REPORT = "report_short.json"

    FULL_REPORT = "report_full.json"
    SCHEMA_INFERRED = "inferred_schema.json"


class ApiEndpoint(Enum):
    """
    Enum API endpoints.
    """

    RUN = "run-metadata/"
    DATA_RESOURCE = "data-resource/"
    SHORT_REPORT = "short-report/"


class MetadataType(Enum):
    """
    Enum metadata types denomination.
    """

    RUN_METADATA = "run"
    SHORT_REPORT = "report"
    DATA_RESOURCE = "resource"
    ARTIFACT = "artifact"
    DATA_PACKAGE = "package"
