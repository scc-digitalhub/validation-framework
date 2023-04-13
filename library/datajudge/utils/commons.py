"""
Module for common terms definition.
"""
# Datajudge version
DATAJUDGE_VERSION = ""


# Libraries
LIBRARY_FRICTIONLESS = "frictionless"
LIBRARY_PANDAS_PROFILING = "pandas_profiling"
LIBRARY_YDATA_PROFILING = "ydata_profiling"
LIBRARY_DUCKDB = "duckdb"
LIBRARY_SQLALCHEMY = "sqlalchemy"
LIBRARY_SQL_GENERIC = "sql"
LIBRARY_GREAT_EXPECTATIONS = "great_expectations"
LIBRARY_DUMMY = "_dummy"


# Data readers format
DATAREADER_FILE = "file"
DATAREADER_NATIVE = "native"
DATAREADER_BUFFER = "buffer"


# Store types
STORE_DUMMY = "_dummy"
STORE_LOCAL = "local"
STORE_HTTP = "http"
STORE_FTP = "ftp"
STORE_S3 = "s3"
STORE_AZURE = "azure"
STORE_SQL = "sql"
STORE_ODBC = "odbc"


# Schemes
SCHEME_LOCAL = [
    "",
    "file",
]
SCHEME_HTTP = [
    "http",
    "https",
]
SCHEME_S3 = [
    "s3",
]
SCHEME_AZURE = [
    "wasb",
    "wasbs",
]
SCHEME_FTP = [
    "ftp",
]
SCHEME_SQL = [
    "sql",
    "postgresql",
    "mysql",
    "mssql",
    "oracle",
    "sqlite",
]
SCHEME_ODBC = [
    "dremio",
    "odbc",
]
SCHEME_DUCKDB = [
    "duckdb",
]
SCHEME_DUMMY = [
    "_dummy",
]


# Constraints

# Frictionless
CONSTRAINT_FRICTIONLESS_SCHEMA = "frictionless_schema"

# SQL constraints expectation
CONSTRAINT_SQL_EMPTY = "empty"
CONSTRAINT_SQL_NON_EMPTY = "non-empty"
CONSTRAINT_SQL_EXACT = "exact"
CONSTRAINT_SQL_RANGE = "range"
CONSTRAINT_SQL_MINIMUM = "minimum"
CONSTRAINT_SQL_MAXIMUM = "maximum"

#  SQL constraint dats to check
CONSTRAINT_SQL_CHECK_VALUE = "value"
CONSTRAINT_SQL_CHECK_ROWS = "rows"


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
OPERATION_INFERENCE = "inference"
OPERATION_PROFILING = "profiling"
OPERATION_VALIDATION = "validation"


# Result typology
RESULT_WRAPPED = "wrapped"
RESULT_DATAJUDGE = "datajudge"
RESULT_RENDERED = "rendered"
RESULT_LIBRARY = "library"


# Execution status
STATUS_INIT = "created"
STATUS_RUNNING = "executing"
STATUS_INTERRUPTED = "interrupdted"
STATUS_FINISHED = "finished"
STATUS_ERROR = "error"


# Generics
GENERIC_DUMMY = "_dummy"
DEFAULT_DIRECTORY = "./djruns/tmp"
DEFAULT_PROJECT = "project"
DEFAULT_EXPERIMENT = "experiment"
