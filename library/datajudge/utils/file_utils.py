"""
Common filesystem utils.
"""
import os
import shutil
from pathlib import Path


# Directories


def check_dir(path: str) -> bool:
    """
    Check if a directory exists.
    """
    try:
        return Path(path).is_dir()
    except OSError:
        return False


def make_dir(*args) -> None:
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


def check_make_dir(uri: str) -> None:
    """
    Check if a directory already exist, otherwise create it.
    """
    if not check_dir(uri):
        make_dir(uri)


# Files


def check_path(path: str) -> bool:
    """
    Check if the resource exists.
    """
    try:
        return Path(path).exists()
    except OSError:
        return False


def copy_file(src: str, dst: str) -> None:
    """
    Copy local file to destination.
    """
    shutil.copy(src, dst)


def clean_all(path: str) -> None:
    """
    Remove dir and all it's contents.
    """
    shutil.rmtree(path)
