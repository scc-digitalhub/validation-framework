from datajudge.run.plugin.inference.dummy_inference import \
    InferenceBuilderDummy
from datajudge.run.plugin.inference.frictionless_inference import \
    InferenceBuilderFrictionless
from datajudge.run.plugin.profiling.dummy_profiling import \
    ProfileBuilderDummy
from datajudge.run.plugin.profiling.frictionless_profiling import \
    ProfileBuilderFrictionless
from datajudge.run.plugin.profiling.great_expectation_profiling import \
    ProfileBuilderGreatExpectation
from datajudge.run.plugin.profiling.pandas_profiling_profiling import \
    ProfileBuilderPandasProfiling
from datajudge.run.plugin.validation.duckdb_validation import \
    ValidationBuilderDuckDB
from datajudge.run.plugin.validation.dummy_validation import \
    ValidationBuilderDummy
from datajudge.run.plugin.validation.frictionless_validation import \
    ValidationBuilderFrictionless
from datajudge.run.plugin.validation.great_expectation_validation import \
    ValidationBuilderGreatExpectation
from datajudge.run.plugin.validation.sqlalchemy_validation import \
    ValidationBuilderSqlAlchemy
from datajudge.utils.commons import (LIBRARY_DUCKDB, LIBRARY_DUMMY,
                                     LIBRARY_FRICTIONLESS,
                                     LIBRARY_GREAT_EXPECTATION,
                                     LIBRARY_PANDAS_PROFILING,
                                     LIBRARY_SQLALCHEMY, OPERATION_INFERENCE,
                                     OPERATION_PROFILING, OPERATION_VALIDATION)

REGISTRY = {
    OPERATION_INFERENCE: {
        LIBRARY_DUMMY: InferenceBuilderDummy,
        LIBRARY_FRICTIONLESS: InferenceBuilderFrictionless,
    },
    OPERATION_PROFILING: {
        LIBRARY_DUMMY: ProfileBuilderDummy,
        LIBRARY_FRICTIONLESS: ProfileBuilderFrictionless,
        LIBRARY_GREAT_EXPECTATION: ProfileBuilderGreatExpectation,
        LIBRARY_PANDAS_PROFILING: ProfileBuilderPandasProfiling,
    },
    OPERATION_VALIDATION: {
        LIBRARY_DUCKDB: ValidationBuilderDuckDB,
        LIBRARY_DUMMY: ValidationBuilderDummy,
        LIBRARY_FRICTIONLESS: ValidationBuilderFrictionless,
        LIBRARY_GREAT_EXPECTATION: ValidationBuilderGreatExpectation,
        LIBRARY_SQLALCHEMY: ValidationBuilderSqlAlchemy,
    },
}
