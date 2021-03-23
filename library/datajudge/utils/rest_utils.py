import json
from urllib.parse import urljoin, urlparse

import requests


def api_post_call(data: dict, uri: str) -> dict:
    """
    REST POST call.
    """
    data = json.dumps(data)
    return requests.post(uri, data=data)


def api_put_call(data: dict, uri: str) -> None:
    """
    REST PUT call.
    """
    data = json.dumps(data)
    return requests.put(uri, data=data)


def api_get_call(uri: str) -> None:
    """
    REST GET call.
    """
    return requests.get(uri)


def api_delete_call() -> None:
    """
    REST DELETE call.
    """
    pass


def parse_url(url: str):
    """
    Parse an URL and clean it from double '/' character.
    """
    return urljoin(url,
                   urlparse(url).path.replace('//','/'))
