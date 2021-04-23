"""
Common file utils.
"""
import glob
import gzip
import json
import os
import shutil
from io import BytesIO
from pathlib import Path
from typing import IO, Union

from datajudge.utils.io_utils import wrap_bytes


# Directories

def check_dir(path: str) -> bool:
    """
    Check if a directory exists.
    """
    if Path(path).is_dir():
        return True
    return False


def check_abs_path(path: str) -> bool:
    """
    Check if a path is absolute.
    """
    if Path(path).is_absolute():
        return True
    return False


def make_dir(*args):
    """
    Dirs builder function.
    """
    try:
        os.makedirs(get_absolute_path(*args))
    except Exception as ex:
        raise ex


def get_absolute_path(*args) -> str:
    """
    Return absolute path.
    """
    return str(Path(*args).absolute())


def get_path(*args) -> str:
    """
    Return path.
    """
    return str(Path(*args))


# Files

def check_file(path: str) -> bool:
    """
    Check if the resource is a file.
    """
    if Path(path).is_file():
        return True
    return False


def check_file_dimension(file_uri: str) -> int:
    """
    Return the file dimension in bytes.
    """
    return Path(file_uri).stat().st_size


def copy_file(src: str, dst: str) -> None:
    """
    Copy local file to destination.
    """
    shutil.copy(src, dst)


def get_file_name(src: str) -> None:
    """
    Get file name of a resource.
    """
    if check_file(src):
        return Path(src).name
    return "Unnamed-file"


def remove_files(path: str) -> None:
    """
    Remove files from a folder.
    """
    if not path.endswith("*"):
        path = get_path(path, "*")
    files = glob.glob(path)
    for file in files:
        os.remove(file)


# Json

def write_json(data: dict,
               path: Union[str, Path]) -> None:
    """
    Store JSON file.
    """
    with open(path, "w") as file:
        json.dump(data, file)


def read_json(path: Union[str, Path]) -> dict:
    """
    Read JSON file.
    """
    with open(path) as file:
        json_dict = json.load(file)
    return json_dict


# Fileobj

def write_object(buff: IO,
                 dst: str) -> None:
    """
    Save a buffer as file.
    """
    buff.seek(0)
    if isinstance(buff, BytesIO):
        buff = wrap_bytes(buff)
    with open(dst, "w") as file:
        shutil.copyfileobj(buff, file)


def open_file(path: str) -> IO:
    """
    Open file and return a buffer.
    """
    buffer = BytesIO()
    if path.endswith(".gz"):
        with gzip.open(path, "rb") as file:
            buffer.write(file.read())
    else:
        with open(path, "rb") as file:
            buffer.write(file.read())
    buffer.seek(0)
    return buffer
