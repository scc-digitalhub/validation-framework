import requests
import json
from urllib.parse import urlparse, urljoin


def api_post_call(data: dict, uri: str) -> dict:
    data = json.dumps(data)
    return requests.post(uri, data=data)


def api_put_call(data: dict, uri: str) -> None:
    data = json.dumps(data)
    return requests.put(uri, data=data)


def api_get_call(uri: str) -> None:
    return requests.get(uri)


def api_delete_call() -> None:
    pass


def parse_url(url: str):
    """Parse an URL and clean it from
    double slash character."""
    return urljoin(url,
                   urlparse(url).path.replace('//','/'))
