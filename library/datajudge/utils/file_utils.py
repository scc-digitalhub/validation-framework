"""
Common filesystem utils.
"""
import glob
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


def check_abs_path(path: str) -> bool:
    """
    Check if a path is absolute.
    """
    try:
        return Path(path).is_absolute()
    except OSError:
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


def check_make_dir(uri: str) -> None:
    """
    Check if a directory already exist, otherwise create it.
    """
    if not check_dir(uri):
        make_dir(uri)


# Files

def check_file(path: str) -> bool:
    """
    Check if the resource is a file.
    """
    try:
        return Path(path).is_file()
    except OSError:
        return False


def check_path(path: str) -> bool:
    """
    Check if the resource exists.
    """
    try:
        return Path(path).exists()
    except OSError:
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


def clean_all(path: str) -> None:
    """
    Remove dir and all it's contents.
    """
    shutil.rmtree(path)
