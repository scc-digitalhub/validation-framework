import os
import urllib.parse
from typing import Optional, Tuple

from datajudge.utils.constants import StoreType
from datajudge.utils.file_utils import get_absolute_path
from datajudge.utils.s3_utils import build_s3_uri
from datajudge.utils.rest_utils import parse_url


LOCAL_SCHEME = ["", "file"]
REST_SCHEME = ["http", "https"]
S3_SCHEME = ["s3"]

DEFAULT_LOCAL = "./validruns"


def build_exp_uri(scheme: str,
                  uri: str,
                  experiment_id: str,
                  store: str,
                  project_id: Optional[str] = None) -> str:
    """
    Build experiment URI.
    """

    # Metadata stores
    if store == StoreType.METADATA.value:

        if scheme in LOCAL_SCHEME:
            return get_absolute_path(uri, store, experiment_id)

        elif scheme in REST_SCHEME:
            if project_id is not None:
                return parse_url(uri + f"/api/project/{project_id}")
            raise RuntimeError("'project_id' needed!")

        raise NotImplementedError

    # Artifact/data stores
    elif store in (StoreType.DATA.value, StoreType.ARTIFACT.value):

        if scheme in LOCAL_SCHEME:
            return get_absolute_path(uri, store, experiment_id)

        elif scheme in S3_SCHEME:
            return build_s3_uri(uri, store, experiment_id)

        raise NotImplementedError

    else:
        raise RuntimeError("Invalid store.")


def resolve_uri(uri: str,
                experiment_id: str,
                store: str,
                project_id: Optional[str] = None) -> Tuple[str, str]:
    """
    Return a builded URI and it's scheme.
    """
    uri = uri if uri is not None else DEFAULT_LOCAL
    scheme = get_scheme(uri)
    new_uri = build_exp_uri(scheme, uri, experiment_id, store, project_id)
    return new_uri, scheme


def get_scheme(uri: str) -> str:
    """
    Get scheme of an URI.
    """
    return urllib.parse.urlparse(uri).scheme


def check_local_scheme(uri: str) -> bool:
    """
    Check if URI point to local filesystem.
    """
    if get_scheme(uri) in LOCAL_SCHEME:
        return True
    return False


def get_name_from_uri(uri: str) -> str:
    """
    Return filename from uri.
    """
    parsed = urllib.parse.urlparse(uri).path
    return os.path.basename(parsed)
