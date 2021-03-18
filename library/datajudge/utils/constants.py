from enum import Enum


class ClientDefault(Enum):
    # Default names
    EXP_NAME = "DefaultExp"
    PROJ_ID = "DefaultProj"
    STORE_URI = "./validruns"
    CREDENTIALS = None


class OutputDesc(Enum):
    ARTIFACT = "artifact"
    METADATA = "metadata"


class FileNames(Enum):
    # Metadata file names
    RUN_METADATA = "run_metadata.json"
    DATA_RESOURCE = "data_resource.json"
    SHORT_REPORT = "report_short.json"
    # Artifacts file names
    FULL_REPORT = "report_full.json"
    SCHEMA_INFERRED = "inferred_schema.json"

    
class ApiEndpoint(Enum):
    RUN = "run-metadata/"
    DATA_RESOURCE = "data-resource/"
    SHORT_REPORT = "short-report/"


class MetadataType(Enum):
    RUN_METADATA = "run"
    SHORT_REPORT = "report"
    DATA_RESOURCE = "resource"
    ARTIFACT = "artifact"
    DATA_PACKAGE = "package"
