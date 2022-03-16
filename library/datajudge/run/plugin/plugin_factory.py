"""
Plugin factory module.
"""
from datajudge.run.plugin import (InferenceBuilderDummy,
                                  InferenceBuilderFrictionless,
                                  ProfileBuilderDummy,
                                  ProfileBuilderFrictionless,
                                  ProfileBuilderPandasProfiling,
                                  ValidationBuilderDummy,
                                  ValidationBuilderFrictionless)
from datajudge.utils import config as cfg
from datajudge.utils.utils import listify


BUILDER_REGISTRY = {
    cfg.OP_INF: {
        "dummy": InferenceBuilderDummy,
        "frictionless": InferenceBuilderFrictionless,
        },
    cfg.OP_VAL: {
        "dummy": ValidationBuilderDummy,
        "frictionless": ValidationBuilderFrictionless,
        },
    cfg.OP_PRO: {
        "dummy": ProfileBuilderDummy,
        "frictionless": ProfileBuilderFrictionless,
        "pandas_profiling": ProfileBuilderPandasProfiling,
        },
    "snapshot": {
    }
}


def get_builder(config: dict,
                typology: str) -> list:
    """
    Factory method that creates plugin builders.
    """
    builders = {}
    if config.get("enabled", False):
        library = config.get("library")
        for lib in listify(library):
            try:
                builders[lib] = BUILDER_REGISTRY[typology][lib]()
            except KeyError as k_err:
                raise NotImplementedError from k_err
        return builders
    builders["dummy"] = BUILDER_REGISTRY[typology]["dummy"]()
    return builders
