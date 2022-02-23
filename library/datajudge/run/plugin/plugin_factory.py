"""
Run plugin factory.
"""
# pylint: disable=import-error,invalid-name
from typing import Any, List

from datajudge.run.plugin.inference import (InferencePluginDummy,
                                            InferencePluginFrictionless)
from datajudge.run.plugin.profiling import (ProfilePluginDummy,
                                            ProfilePluginFrictionless,
                                            ProfilePluginPandasProfiling)
from datajudge.run.plugin.validation import (ValidationPluginDummy,
                                             ValidationPluginFrictionless)


PLUGINS = {
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
        "frictionless": ProfilePluginFrictionless,
        "pandas_profiling": ProfilePluginPandasProfiling,
        },
    "snapshot": {
    }
}


def get_plugin(config: List[dict],
               typology: str) -> Any:
    """
    Factory method that returns a run plugin.
    """
    if config is None:
        return PLUGINS[typology]["dummy"]()
    if config.enabled:
        try:
            return PLUGINS[typology][config.library]()
        except KeyError as k_err:
            raise NotImplementedError from k_err
    return PLUGINS[typology]["dummy"]()
