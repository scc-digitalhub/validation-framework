"""
Common REST utils.
"""
# pylint: disable=import-error
import requests
from requests.models import HTTPError, Response


def api_get_call(url: str,
                 **kwargs: dict) -> Response:
    """
    REST GET call.
    """
    try:
        return requests.get(url, **kwargs)
    except Exception as ex:
        raise ex


def api_post_call(url: str,
                  **kwargs: dict) -> Response:
    """
    REST POST call.
    """
    try:
        return requests.post(url, **kwargs)
    except Exception as ex:
        raise ex


def api_put_call(url: str,
                 **kwargs: dict) -> Response:
    """
    REST PUT call.
    """
    try:
        return requests.put(url, **kwargs)
    except Exception as ex:
        raise ex


def check_url_availability(url: str) -> None:
    """
    Check URL availability.
    """
    try:
        response = requests.head(url)
        if response.status_code != 200:
            raise HTTPError("Something wrong, response code ",
                            f"{response.status_code} for url ",
                            f"{url}.")
    except Exception as ex:
        raise ex
