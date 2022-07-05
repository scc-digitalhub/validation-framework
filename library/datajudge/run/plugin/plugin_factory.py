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
                                  ProfileBuilderPandasProfiling,
                                  ProfileBuilderGreatExpectation,
                                  ValidationBuilderDuckDB,
                                  ValidationBuilderDummy,
                                  ValidationBuilderFrictionless,
                                  ValidationBuilderSqlAlchemy,
                                  ValidationBuilderGreatExpectation)
from datajudge.utils.commons import (DUCKDB, DUMMY, FRICTIONLESS, GREAT_EXPECTATION, INFERENCE,
                                    PROFILING, SQLALCHEMY, VALIDATION, PANDAS_PROFILING)

if typing.TYPE_CHECKING:
    from datajudge.utils.config import ExecConfig


REGISTRY = {
    INFERENCE: {
        DUMMY: InferenceBuilderDummy,
        FRICTIONLESS: InferenceBuilderFrictionless,
        },
    VALIDATION: {
        DUMMY: ValidationBuilderDummy,
        DUCKDB: ValidationBuilderDuckDB,
        FRICTIONLESS: ValidationBuilderFrictionless,
        SQLALCHEMY: ValidationBuilderSqlAlchemy,
        GREAT_EXPECTATION: ValidationBuilderGreatExpectation,
        },
    PROFILING: {
        DUMMY: ProfileBuilderDummy,
        FRICTIONLESS: ProfileBuilderFrictionless,
        PANDAS_PROFILING: ProfileBuilderPandasProfiling,
        GREAT_EXPECTATION: ProfileBuilderGreatExpectation,
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
            builders.append(REGISTRY[typology][cfg.library](cfg.execArgs,
                                                            cfg.tmpFormat,
                                                            stores))
        except KeyError:
            raise NotImplementedError
    return builders
