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


def get_plugin(config: dict,
               typology: str) -> list:
    """
    Factory method that creates run plugins.
    """
    plugin_list = {}
    if config is None:
        plugin_list["dummy"] = PLUGINS[typology]["dummy"]()
        return plugin_list
    if config.enabled:
        if not isinstance(config.library, list):
            config.library = [config.library]
        for lib in config.library:
            try:
                plugin_list[lib] = PLUGINS[typology][lib]()
            except KeyError as k_err:
                raise NotImplementedError from k_err
        return plugin_list
    plugin_list["dummy"] = PLUGINS[typology]["dummy"]()
    return plugin_list
