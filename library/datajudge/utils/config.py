"""
Configuration for filenames, endpoints, etc.
"""
from typing import Optional, Union
from pydantic import BaseModel


class FrictionlessConstraint(BaseModel):
    pass


class DatajudgeConstraint(BaseModel):
    pass


Constraints = Union[FrictionlessConstraint,
                    DatajudgeConstraint]


class ValidationConfig(BaseModel):
    enabled: bool = True
    library: Optional[str] = None
    constraints: Optional[Constraints] = None


class InferenceConfig(BaseModel):
    enabled: bool = True
    library: Optional[str] = None


class ProfilingConfig(BaseModel):
    enabled: bool = True
    library: Optional[str] = None


class SnapshotConfig(BaseModel):
    enabled: bool = False


Configs = Union[ValidationConfig,
                InferenceConfig,
                ProfilingConfig,
                SnapshotConfig]


class RunConfig(BaseModel):

    validation: Optional[ValidationConfig] = ValidationConfig()
    inference: Optional[InferenceConfig] = InferenceConfig()
    profiling: Optional[ProfilingConfig] = ProfilingConfig()
    snapshot: Optional[SnapshotConfig] = SnapshotConfig()


# DATAJUDGE VERSION
DATAJUDGE_VERSION = "1.1.0"

# FILENAMES METADATA
FN_RUN_METADATA = "run_metadata.json"
FN_DATA_RESOURCE = "data_resource.json"
FN_SHORT_REPORT = "report_short.json"
FN_SHORT_SCHEMA = "schema_short.json"
FN_DATA_PROFILE = "data_profile.json"
FN_ARTIFACT_METADATA = "artifact_metadata_{}.json"
FN_RUN_ENV = "run_env.json"

# FILENAMES ARTIFACTS
FN_VALID_SCHEMA = "table_schema.json"
FN_FULL_REPORT = "report_full.json"
FN_INFERRED_SCHEMA = "inferred_schema.json"
FN_FULL_PROFILE_HTML = "profile_report.html"
FN_FULL_PROFILE_JSON = "profile_report.json"

# API ENDPOINTS
API_BASE = "/api/project/"
API_RUN_METADATA = "/run-metadata"
API_DATA_RESOURCE = "/data-resource"
API_SHORT_REPORT = "/short-report"
API_SHORT_SCHEMA = "/short-schema"
API_DATA_PROFILE = "/data-profile"
API_ARTIFACT_METADATA = "/artifact-metadata"
API_RUN_ENV = "/run-environment"

# METADATA TYPE
MT_RUN_METADATA = "run"
MT_DATA_RESOURCE = "resource"
MT_SHORT_REPORT = "report"
MT_SHORT_SCHEMA = "schema"
MT_DATA_PROFILE = "profile"
MT_ARTIFACT_METADATA = "artifact"
MT_RUN_ENV = "run_env"

# STORE TYPE
ST_METADATA = "metadata"
ST_ARTIFACT = "artifact"
ST_DATA = "data"

# DEFAULT FOLDERS
DEFAULT_LOCAL = "./djruns"
DEFAULT_TMP = DEFAULT_LOCAL + "/tmp"

# DEFAULT NAMES
DEFAULT_PROJ = "project"
DEFAULT_EXP = "experiment"
