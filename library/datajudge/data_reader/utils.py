"""
Utils functions for data reader.
"""
from datajudge.data_reader.registry import REGISTRY


def get_reader(reader_type: str) -> "DataReader":
    """
    Registry getter.
    """
    try:
        return REGISTRY[reader_type]
    except KeyError:
        raise NotImplementedError


def build_reader(
    reader_type: str,
    store: "ArtifactStore",
    **kwargs,
) -> "DataReader":
    """
    Reader builder.
    """
    return get_reader(reader_type)(store, **kwargs)
