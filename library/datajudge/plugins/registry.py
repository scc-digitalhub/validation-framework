"""
PluginBuilder registry.
"""
from datajudge.plugins.inference.dummy_inference import InferenceBuilderDummy
from datajudge.plugins.inference.frictionless_inference import (
    InferenceBuilderFrictionless,
)
from datajudge.plugins.profiling.dummy_profiling import ProfileBuilderDummy
from datajudge.plugins.profiling.frictionless_profiling import (
    ProfileBuilderFrictionless,
)
from datajudge.plugins.profiling.great_expectations_profiling import (
    ProfileBuilderGreatExpectations,
)
from datajudge.plugins.profiling.pandas_profiling_profiling import (
    ProfileBuilderPandasProfiling,
)
from datajudge.plugins.profiling.ydata_profiling_profiling import (
    ProfileBuilderYdataProfiling,
)
from datajudge.plugins.validation.duckdb_validation import ValidationBuilderDuckDB
from datajudge.plugins.validation.dummy_validation import ValidationBuilderDummy
from datajudge.plugins.validation.frictionless_validation import (
    ValidationBuilderFrictionless,
)
from datajudge.plugins.validation.great_expectations_validation import (
    ValidationBuilderGreatExpectations,
)
from datajudge.plugins.validation.sqlalchemy_validation import (
    ValidationBuilderSqlAlchemy,
)
from datajudge.utils.commons import (
    LIBRARY_DUCKDB,
    LIBRARY_DUMMY,
    LIBRARY_FRICTIONLESS,
    LIBRARY_GREAT_EXPECTATIONS,
    LIBRARY_PANDAS_PROFILING,
    LIBRARY_YDATA_PROFILING,
    LIBRARY_SQLALCHEMY,
    OPERATION_INFERENCE,
    OPERATION_PROFILING,
    OPERATION_VALIDATION,
)

REGISTRY = {
    OPERATION_INFERENCE: {
        LIBRARY_DUMMY: InferenceBuilderDummy,
        LIBRARY_FRICTIONLESS: InferenceBuilderFrictionless,
    },
    OPERATION_PROFILING: {
        LIBRARY_DUMMY: ProfileBuilderDummy,
        LIBRARY_FRICTIONLESS: ProfileBuilderFrictionless,
        LIBRARY_GREAT_EXPECTATIONS: ProfileBuilderGreatExpectations,
        LIBRARY_PANDAS_PROFILING: ProfileBuilderPandasProfiling,
        LIBRARY_YDATA_PROFILING: ProfileBuilderYdataProfiling,
    },
    OPERATION_VALIDATION: {
        LIBRARY_DUCKDB: ValidationBuilderDuckDB,
        LIBRARY_DUMMY: ValidationBuilderDummy,
        LIBRARY_FRICTIONLESS: ValidationBuilderFrictionless,
        LIBRARY_GREAT_EXPECTATIONS: ValidationBuilderGreatExpectations,
        LIBRARY_SQLALCHEMY: ValidationBuilderSqlAlchemy,
    },
}
