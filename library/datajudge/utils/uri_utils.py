"""
Common URI utils.
"""
from pathlib import Path
from urllib.parse import ParseResult, urlparse, urlunparse


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


def rebuild_uri(uri: str, *args) -> str:
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
