"""
PluginBuilder registry.
"""
# Dummy imports
from datajudge.plugins.inference.dummy_inference import InferenceBuilderDummy
from datajudge.plugins.profiling.dummy_profiling import ProfileBuilderDummy
from datajudge.plugins.validation.dummy_validation import ValidationBuilderDummy
from datajudge.utils.commons import (
    LIBRARY_DUMMY,
    OPERATION_INFERENCE,
    OPERATION_PROFILING,
    OPERATION_VALIDATION,
)

# Registry of plugin builders

REGISTRY = {
    OPERATION_INFERENCE: {
        LIBRARY_DUMMY: InferenceBuilderDummy,
    },
    OPERATION_PROFILING: {
        LIBRARY_DUMMY: ProfileBuilderDummy,
    },
    OPERATION_VALIDATION: {
        LIBRARY_DUMMY: ValidationBuilderDummy,
    },
}


# frictionless imports
try:
    from datajudge.plugins.inference.frictionless_inference import (
        InferenceBuilderFrictionless,
    )
    from datajudge.plugins.profiling.frictionless_profiling import (
        ProfileBuilderFrictionless,
    )
    from datajudge.plugins.validation.frictionless_validation import (
        ValidationBuilderFrictionless,
    )
    from datajudge.utils.commons import LIBRARY_FRICTIONLESS

    REGISTRY[OPERATION_INFERENCE][LIBRARY_FRICTIONLESS] = InferenceBuilderFrictionless
    REGISTRY[OPERATION_PROFILING][LIBRARY_FRICTIONLESS] = ProfileBuilderFrictionless
    REGISTRY[OPERATION_VALIDATION][LIBRARY_FRICTIONLESS] = ValidationBuilderFrictionless

except ImportError:
    ...

# great_expectations imports
try:
    from datajudge.plugins.profiling.great_expectations_profiling import (
        ProfileBuilderGreatExpectations,
    )
    from datajudge.plugins.validation.great_expectations_validation import (
        ValidationBuilderGreatExpectations,
    )
    from datajudge.utils.commons import LIBRARY_GREAT_EXPECTATIONS

    REGISTRY[OPERATION_PROFILING][
        LIBRARY_GREAT_EXPECTATIONS
    ] = ProfileBuilderGreatExpectations
    REGISTRY[OPERATION_VALIDATION][
        LIBRARY_GREAT_EXPECTATIONS
    ] = ValidationBuilderGreatExpectations

except ImportError:
    ...

# pandas_profiling imports
try:
    from datajudge.plugins.profiling.pandas_profiling_profiling import (
        ProfileBuilderPandasProfiling,
    )
    from datajudge.utils.commons import LIBRARY_PANDAS_PROFILING

    REGISTRY[OPERATION_PROFILING][
        LIBRARY_PANDAS_PROFILING
    ] = ProfileBuilderPandasProfiling

except ImportError:
    ...

# ydata_profiling imports
try:
    from datajudge.plugins.profiling.ydata_profiling_profiling import (
        ProfileBuilderYdataProfiling,
    )
    from datajudge.utils.commons import LIBRARY_YDATA_PROFILING

    REGISTRY[OPERATION_PROFILING][
        LIBRARY_YDATA_PROFILING
    ] = ProfileBuilderYdataProfiling

except ImportError:
    ...

# duckdb imports
try:
    from datajudge.plugins.validation.duckdb_validation import ValidationBuilderDuckDB
    from datajudge.utils.commons import LIBRARY_DUCKDB

    REGISTRY[OPERATION_VALIDATION][LIBRARY_DUCKDB] = ValidationBuilderDuckDB

except ImportError:
    ...

# sqlalchemy imports
try:
    from datajudge.plugins.validation.sqlalchemy_validation import (
        ValidationBuilderSqlAlchemy,
    )
    from datajudge.utils.commons import LIBRARY_SQLALCHEMY

    REGISTRY[OPERATION_VALIDATION][LIBRARY_SQLALCHEMY] = ValidationBuilderSqlAlchemy

except ImportError:
    ...
