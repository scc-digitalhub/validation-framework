import json
import os
import shutil
from pathlib import Path
from typing import Union


# Directories

def check_dir(path: str) -> bool:
    """Check if a directory exists."""
    if Path(path).is_dir():
        return True
    return False


def check_abs_path(path: str) -> bool:
    """Check if a path is absolute."""
    if Path(path).is_absolute():
        return True
    return False


def make_dir(*args):
    """Dirs builder function."""
    try:
        os.makedirs(get_absolute_path(*args))
    except Exception as ex:
        raise ex


def get_absolute_path(*args) -> str:
    """Return absolute path."""
    return str(Path(*args).absolute())


def get_path(*args) -> str:
    """Return path."""
    return str(Path(*args))


# Files

def check_file(path: str) -> bool:
    """Check if the resource is a file."""
    if Path(path).is_file():
        return True
    return False


def check_file_dimension(file_uri: str) -> int:
    """Return the file dimension in bytes"""
    return Path(file_uri).stat().st_size


def copy_file(src: str, dst: str) -> None:
    """Copy local file with shutil.copy2"""
    shutil.copy(src, dst)


# Json

def write_json(data: dict,
               path: Union[str, Path]) -> None:
    """Store json file."""
    with open(path, "w") as file:
        json.dump(data, file)


def read_json(path: Union[str, Path]) -> dict:
    """Read json file."""
    with open(path) as file:
        json_dict = json.load(file)
    return json_dict
