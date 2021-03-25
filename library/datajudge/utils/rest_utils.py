import json
from typing import Optional
from urllib.parse import urljoin, urlparse

import requests


def api_post_call(data: dict,
                  uri: str,
                  params: Optional[dict] = None) -> dict:
    """
    REST POST call.
    """
    data = json.dumps(data)
    try:
        return requests.post(uri, data=data, params=params)
    except Exception as ex:
        raise ex


def api_put_call(data: dict, uri: str) -> None:
    """
    REST PUT call.
    """
    data = json.dumps(data)
    try:
        return requests.put(uri, data=data)
    except Exception as ex:
        raise ex


def parse_url(url: str):
    """
    Parse an URL and clean it from double '/' character.
    """
    return urljoin(url, urlparse(url).path.replace('//', '/'))
