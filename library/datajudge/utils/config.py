"""
Configuration for filenames, endpoints, etc.
"""

# FILENAMES METADATA
FN_RUN_METADATA = "run_metadata.json"
FN_DATA_RESOURCE = "data_resource.json"
FN_SHORT_REPORT = "report_short.json"
FN_SHORT_SCHEMA = "schema_short.json"
FN_DATA_PROFILE = "data_profile.json"
FN_ARTIFACT_METADATA = "artifact_metadata_{}.json"

# FILENAMES ARTIFACTS
FN_VALID_SCHEMA = "table_schema.json"
FN_FULL_REPORT = "report_full.json"
FN_INFERRED_SCHEMA = "inferred_schema.json"
FN_FULL_PROFILE = "profile_report.html"

# API ENDPOINTS
API_BASE = "/api/project/"
API_RUN_METADATA = "/run-metadata"
API_DATA_RESOURCE = "/data-resource"
API_SHORT_REPORT = "/short-report"
API_SHORT_SCHEMA = "/short-schema"
API_DATA_PROFILE = "/data-profile"
API_ARTIFACT_METADATA = "/artifact-metadata"

# METADATA TYPE
MT_RUN_METADATA = "run"
MT_DATA_RESOURCE = "resource"
MT_SHORT_REPORT = "report"
MT_SHORT_SCHEMA = "schema"
MT_DATA_PROFILE = "profile"
MT_ARTIFACT_METADATA = "artifact"

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

# SCHEMES
LOCAL_SCHEME = ["", "file"]
REST_SCHEME = ["http", "https"]
S3_SCHEME = ["s3"]
AZURE_SCHEME = ["wasb", "wasbs"]
