# pylint: disable=import-error,invalid-name
from typing import Any

from datajudge.run.inference import (InferencePluginFrictionless, InferencePluginDummy)
from datajudge.run.validation import (ValidationPluginFrictionless, ValidationPluginDummy)
from datajudge.run.profiling import (ProfilePluginPandasProfiling,
                                     ProfilePluginFrictionless, ProfilePluginDummy)


PLUGIN_REGISTRY = {
    "inference": {
        "dummy": InferencePluginDummy,
        "frictionless": InferencePluginFrictionless,
        },
    "validation": {
        "dummy": ValidationPluginDummy,
        "frictionless": ValidationPluginFrictionless,
        },
    "profiling": {
        "dummy": ProfilePluginDummy,
        "pandas_profiling": ProfilePluginPandasProfiling,
        "frictionless": ProfilePluginFrictionless,
        },
    "snapshot": {
        "dummy": None,
    }
}


def get_plugin(config: dict,
               typology: str) -> Any:
    """
    Factory method that returns a run plugin.
    """
    if config is None:
        return PLUGIN_REGISTRY[typology]["dummy"]()
    if config.enabled:
        try:
            return PLUGIN_REGISTRY[typology][config.library]()
        except KeyError as k_err:
            raise NotImplementedError from k_err
    return PLUGIN_REGISTRY[typology]["dummy"]()
