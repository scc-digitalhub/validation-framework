from pathlib import Path

import pytest

from datajudge.utils.file_utils import (
    check_dir,
    check_path,
    clean_all,
    copy_file,
    get_absolute_path,
    get_path,
    make_dir,
)


def make_temp_file(tmp: str) -> str:
    pth = Path(tmp, "file.txt")
    with open(pth, "w") as file:
        file.write("test")
    return str(pth)


def read_file(pth: str):
    with open(pth, "r") as file:
        return file.read()


def test_check_dir(tmp_path):
    assert check_dir(tmp_path)
    assert not check_dir("/notexist")
    assert not check_dir("file.txt")
    with pytest.raises(TypeError):
        check_dir(1)


def test_make_dir(tmp_path):
    folder = Path(tmp_path, "test")
    assert not Path(folder).is_dir()
    make_dir(folder)
    assert Path(folder).is_dir()
    with pytest.raises(OSError):
        make_dir(folder, "/   bad directory @ name ")


def test_get_absolute_path(tmp_path):
    tmp_pth = make_temp_file(tmp_path)
    abspath = get_absolute_path(tmp_pth)
    assert Path(abspath).is_absolute()


def test_get_path(tmp_path):
    assert isinstance(get_path(tmp_path), str)
    assert str(tmp_path) == get_path(tmp_path)


def test_check_path(tmp_path):
    assert check_path(tmp_path)
    tmp_pth = make_temp_file(tmp_path)
    assert check_path(tmp_pth)
    assert not check_path("notexist.txt")
    assert not check_path("/notexist")
    with pytest.raises(TypeError):
        check_path(1)


def test_copy_file(tmp_path):
    path_1 = Path(make_temp_file(tmp_path))
    path_2 = Path(tmp_path, "copy.txt")
    copy_file(path_1, path_2)
    assert path_2.is_file()
    assert path_1.stat().st_size == path_2.stat().st_size
    content_1 = read_file(path_1)
    content_2 = read_file(path_2)
    assert content_1 == content_2


def test_clean_all(tmp_path):
    pth = Path(tmp_path)
    assert pth.is_dir()
    clean_all(tmp_path)
    assert not pth.exists()
