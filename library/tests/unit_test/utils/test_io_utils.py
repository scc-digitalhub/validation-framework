import json
from io import BytesIO, StringIO, TextIOWrapper
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from datajudge.utils.io_utils import (
    wrap_bytes,
    wrap_string,
    write_bytes,
    write_bytesio,
    write_json,
    write_object,
    write_stringio,
    write_text,
    BytesIOWrapper,
)

FILE_TXT = "test.txt"
FILE_JSON = "test.json"

SRC = "test"
BYT = b"test"
JSON = {"test": True}


def read_cnt(path, mode=None):
    mode = "r" if mode is None else mode
    with open(path, mode) as file:
        return file.read()


def test_wrap_bytes():
    bytes_io = BytesIO(BYT)
    string_io = wrap_bytes(bytes_io)
    assert isinstance(string_io, TextIOWrapper)


def test_wrap_string():
    string_io = StringIO(SRC)
    bytes_io = wrap_string(string_io)
    assert isinstance(bytes_io, BytesIOWrapper)


def test_write_stringio():
    string_io = write_stringio(SRC)
    assert isinstance(string_io, StringIO)


def test_write_bytesio():
    bytes_io = write_bytesio(SRC)
    assert isinstance(bytes_io, BytesIO)


def test_write_json(tmp_path):
    path = Path(tmp_path, FILE_JSON)
    write_json(JSON, path)
    assert json.loads(read_cnt(path)) == JSON


def test_write_text(tmp_path):
    path = Path(tmp_path, FILE_TXT)
    write_text(SRC, path)
    assert read_cnt(path) == SRC


def test_write_bytes(tmp_path):
    path = Path(tmp_path, FILE_TXT)
    write_bytes(BYT, path)
    assert read_cnt(path, "rb") == BYT


def test_write_object(tmp_path):
    path = Path(tmp_path, FILE_TXT)
    string_io = StringIO(SRC)
    write_object(string_io, path)
    assert read_cnt(path) == SRC
