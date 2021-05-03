"""
Common URI utils.
"""
from pathlib import Path
from typing import Optional, Tuple
from urllib.parse import ParseResult, urlparse, urlunparse

from datajudge.utils import config as cfg
from datajudge.utils.file_utils import get_absolute_path
from datajudge.utils.rest_utils import parse_url


def parse_uri(uri: str) -> ParseResult:
    """
    Parse an uri.
    """
    return urlparse(uri)


def get_uri_scheme(uri: str) -> str:
    """
    Get scheme of an URI.
    """
    return parse_uri(uri).scheme


def get_uri_netloc(uri: str) -> str:
    """
    Return URI netloc.
    """
    return parse_uri(uri).netloc


def get_uri_path(uri: str) -> str:
    """
    Return URI path.
    """
    return parse_uri(uri).path


def get_name_from_uri(uri: str) -> str:
    """
    Return filename from uri.
    """
    parsed = parse_uri(uri).path
    return Path(parsed).name


def new_uri_path(uri: str, *args) -> str:
    """
    Rebuild an URI.
    """
    parsed = parse_uri(uri)
    new_path = str(Path(parsed.path, *args))
    new_uri = urlunparse((parsed.scheme,
                          parsed.netloc,
                          new_path,
                          parsed.params,
                          parsed.query,
                          parsed.fragment))
    return new_uri


def build_exp_uri(scheme: str,
                  uri: str,
                  experiment_id: str,
                  store: str,
                  project_id: Optional[str] = None) -> str:
    """
    Build experiment URI.
    """

    # Metadata stores
    if store == cfg.ST_METADATA:

        if scheme in cfg.LOCAL_SCHEME:
            return get_absolute_path(uri, store, experiment_id)

        elif scheme in cfg.REST_SCHEME:
            if project_id is not None:
                url = uri + cfg.API_BASE + project_id
                return parse_url(url)
            raise RuntimeError("'project_id' needed!")

        raise NotImplementedError

    # Artifact/data stores
    elif store in (cfg.ST_DATA, cfg.ST_ARTIFACT):

        if scheme in cfg.LOCAL_SCHEME:
            return get_absolute_path(uri, store, experiment_id)

        elif scheme in cfg.S3_SCHEME:
            return new_uri_path(uri, store, experiment_id)

        elif scheme in cfg.AZURE_SCHEME:
            return new_uri_path(uri, store, experiment_id)

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
    uri = uri if uri is not None else cfg.DEFAULT_LOCAL
    scheme = get_uri_scheme(uri)
    new_uri = build_exp_uri(scheme, uri, experiment_id, store, project_id)
    return new_uri, scheme
