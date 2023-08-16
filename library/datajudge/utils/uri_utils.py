"""
Common URI utils.
"""
from pathlib import Path
from urllib.parse import ParseResult, urljoin, urlparse, urlunparse


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
    return Path(uri).name


def rebuild_uri(uri: str, *args) -> str:
    """
    Rebuild an URI.
    """
    parsed = parse_uri(uri)
    new_path = str(Path(parsed.path, *args))
    new_uri = urlunparse(
        (
            parsed.scheme,
            parsed.netloc,
            new_path,
            parsed.params,
            parsed.query,
            parsed.fragment,
        )
    )
    return new_uri


def build_key(dst: str, *args) -> str:
    """
    Build key to upload objects.
    """
    key = str(Path(get_uri_path(dst), *args))
    if key.startswith("/"):
        key = key[1:]
    return key


def check_url(url: str) -> str:
    """
    Parse an URL and clean it from double '/' character.
    """
    parsed = get_uri_path(url).replace("//", "/")
    return urljoin(url, parsed)
