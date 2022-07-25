"""
Plugin builder factory module.
"""
from __future__ import annotations

import typing
from typing import List

from datajudge.run.plugin import (InferenceBuilderDummy,
                                  InferenceBuilderFrictionless,
                                  ProfileBuilderDummy,
                                  ProfileBuilderFrictionless,
                                  ProfileBuilderGreatExpectation,
                                  ProfileBuilderPandasProfiling,
                                  ValidationBuilderDuckDB,
                                  ValidationBuilderDummy,
                                  ValidationBuilderFrictionless,
                                  ValidationBuilderGreatExpectation,
                                  ValidationBuilderSqlAlchemy)
from datajudge.utils.commons import (LIBRARY_DUCKDB, LIBRARY_DUMMY,
                                     LIBRARY_FRICTIONLESS,
                                     LIBRARY_GREAT_EXPECTATION,
                                     LIBRARY_PANDAS_PROFILING,
                                     LIBRARY_SQLALCHEMY, OPERATION_INFERENCE,
                                     OPERATION_PROFILING, OPERATION_VALIDATION)

if typing.TYPE_CHECKING:
    from datajudge.utils.config import ExecConfig


REGISTRY = {
    OPERATION_INFERENCE: {
        LIBRARY_DUMMY: InferenceBuilderDummy,
        LIBRARY_FRICTIONLESS: InferenceBuilderFrictionless,
    },
    OPERATION_VALIDATION: {
        LIBRARY_DUMMY: ValidationBuilderDummy,
        LIBRARY_DUCKDB: ValidationBuilderDuckDB,
        LIBRARY_FRICTIONLESS: ValidationBuilderFrictionless,
        LIBRARY_SQLALCHEMY: ValidationBuilderSqlAlchemy,
        LIBRARY_GREAT_EXPECTATION: ValidationBuilderGreatExpectation,
    },
    OPERATION_PROFILING: {
        LIBRARY_DUMMY: ProfileBuilderDummy,
        LIBRARY_FRICTIONLESS: ProfileBuilderFrictionless,
        LIBRARY_PANDAS_PROFILING: ProfileBuilderPandasProfiling,
        LIBRARY_GREAT_EXPECTATION: ProfileBuilderGreatExpectation,
    }
}


def builder_factory(config: List[ExecConfig],
                    typology: str,
                    stores: dict
                    ) -> list:
    """
    Factory method that creates plugin builders.
    """
    builders = []
    for cfg in config:
        try:
            builders.append(REGISTRY[typology][cfg.library](stores,
                                                            cfg.fetchMode,
                                                            cfg.readerArgs,
                                                            cfg.execArgs))
        except KeyError:
            raise NotImplementedError
    return builders
