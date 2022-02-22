from datajudge.run.profiling.pandas_profiling import ProfilePluginPandasProfiling
from datajudge.run.profiling.frictionless import ProfilePluginFrictionless
from datajudge.run.profiling.dummy import ProfilePluginDummy

__all__ = [
    "ProfilePluginDummy",
    "ProfilePluginPandasProfiling",
    "ProfilePluginFrictionless"
]
