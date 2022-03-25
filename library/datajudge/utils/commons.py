"""
Module for common terms definition.
"""

# Datajudge version
DATAJUDGE_VERSION = "0.2.0"

# Libraries
DUMMY = "_dummy"
FRICTIONLESS = "frictionless"
PANDAS_PROFILING = "pandas_profiling"
DUCKDB = "duckdb"

# DuckDB sonstraints expectation
EMPTY = "empty"
NON_EMPTY = "non-empty"
EXACT = "exact"
RANGE = "range"
MINIMUM = "minimum"
MAXIMUM = "maximum"

CHECK_VALUE = "value"
CHECK_ROWS = "rows"

# API endpoints
API_BASE = "/api/project/"
API_RUN_METADATA = "/run-metadata"
API_DJ_REPORT = "/short-report"
API_DJ_SCHEMA = "/short-schema"
API_DJ_PROFILE = "/data-profile"
API_ARTIFACT_METADATA = "/artifact-metadata"
API_RUN_ENV = "/run-environment"

# Filenames metadata
FN_RUN_METADATA = "run_metadata.json"
FN_DJ_REPORT = "report_{}.json"
FN_DJ_SCHEMA = "schema_{}.json"
FN_DJ_PROFILE = "profile_{}.json"
FN_ARTIFACT_METADATA = "artifact_metadata_{}.json"
FN_RUN_ENV = "run_env.json"

# Metadata type
MT_RUN_METADATA = "run"
MT_DJ_REPORT = "report"
MT_DJ_SCHEMA = "schema"
MT_DJ_PROFILE = "profile"
MT_ARTIFACT_METADATA = "artifact"
MT_RUN_ENV = "run_env"

# Execution operations
INFERENCE = "inference"
PROFILING = "profiling"
VALIDATION = "validation"

# Result typology
RES_WRAP = "wrapped"
RES_DJ = "datajudge"
RES_RENDER = "rendered"
RES_LIB = "library"


# Execution status
STATUS_INIT = "created"
STATUS_RUNNING = "executing"
STATUS_INTERRUPTED = "interrupdted"
STATUS_FINISHED = "finished"
STATUS_ERROR = "error"
