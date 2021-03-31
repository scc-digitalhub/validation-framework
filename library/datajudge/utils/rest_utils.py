from typing import Any, Optional
from urllib.parse import urljoin, urlparse

import requests
from requests.models import HTTPError, Response  # pylint: disable=import-error


def api_post_call(data: dict,
                  uri: str,
                  config: Optional[dict] = None,
                  params: Optional[dict] = None) -> dict:
    """
    REST POST call.
    """
    auth = parse_auth(config)
    try:
        return requests.post(uri, json=data, auth=auth, params=params)
    except Exception as ex:
        raise ex


def api_put_call(data: dict,
                 uri: str,
                 config: Optional[dict] = None) -> None:
    """
    REST PUT call.
    """
    auth = parse_auth(config)
    try:
        return requests.put(uri, json=data, auth=auth)
    except Exception as ex:
        raise ex


def parse_url(url: str):
    """
    Parse an URL and clean it from double '/' character.
    """
    return urljoin(url, urlparse(url).path.replace('//', '/'))


def parse_auth(config: dict) -> Any:
    if config:
        if config["auth"] == "basic":
            auth = config["user"], config["password"]
        return auth
    return None


def parse_status_code(response: Response) -> None:
    error = str(response.json())
    if response.status_code == 400:
        raise HTTPError(error)
    elif response.status_code == 401:
        raise HTTPError(error)
