"""
Common Azure utils.
"""
# pylint: disable=import-error
from typing import IO

from azure.storage.blob import ContainerClient


def check_container(client: ContainerClient) -> bool:
    """
    Check access to a container.
    """
    return client.exists()


def upload_fileobj(client: ContainerClient,
                   name: str,
                   data: IO,
                   metadata: dict) -> None:
    """
    Upload fileobj to Azure.
    """
    client.upload_blob(name=name,
                       data=data,
                       metadata=metadata,
                       overwrite=True)


def upload_file(client: ContainerClient,
                name: str,
                path: str,
                metadata: dict) -> None:
    """
    Upload file to Azure.
    """
    with open(path, "rb") as file:
        client.upload_blob(name=name,
                           data=file,
                           metadata=metadata,
                           overwrite=True)


def get_object(client: ContainerClient,
               path: str) -> bytes:
    """
    Download object from Azure.
    """
    return client.download_blob(path).readall()
