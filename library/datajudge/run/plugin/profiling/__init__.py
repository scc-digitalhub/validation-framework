from datajudge.run.plugin.profiling.pandas_profiling import \
                                        ProfilePluginPandasProfiling
from datajudge.run.plugin.profiling.frictionless import \
                                        ProfilePluginFrictionless
from datajudge.run.plugin.profiling.dummy import ProfilePluginDummy

__all__ = [
    "ProfilePluginDummy",
    "ProfilePluginPandasProfiling",
    "ProfilePluginFrictionless"
]
