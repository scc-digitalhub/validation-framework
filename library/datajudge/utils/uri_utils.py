import urllib.parse
from typing import Optional, Tuple

from datajudge.utils.file_utils import get_absolute_path
from datajudge.utils.s3_utils import build_s3_uri
from datajudge.utils.rest_utils import parse_url


LOCAL_SCHEME = ["", "file"]
REST_SCHEME = ["http", "https"]
S3_SCHEME = ["s3"]

METADATA = "metadata"
ARTIFACT = "artifact"

DEFAULT_STORE = "./validruns"


def build_exp_uri(scheme: str,
                  uri: str,
                  experiment_id: str,
                  store: str,
                  project_id: Optional[str] = None) -> str:
    """
    Build experiment URI.
    """
    if store == METADATA:
        if scheme in LOCAL_SCHEME:
            return get_absolute_path(uri, METADATA, experiment_id)
        elif scheme in REST_SCHEME and project_id is not None:
            base_url = f"/api/project/{project_id}"
            return parse_url(uri + base_url)
        elif scheme in REST_SCHEME and project_id is None:
            raise RuntimeError("'project_id' needed!")
        raise NotImplementedError

    elif store == ARTIFACT:
        if scheme in LOCAL_SCHEME:
            return get_absolute_path(uri, ARTIFACT, experiment_id)
        elif scheme in S3_SCHEME:
            return build_s3_uri(uri, ARTIFACT, experiment_id)
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
    uri = uri if uri is not None else DEFAULT_STORE
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
