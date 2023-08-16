"""
Common IO utils.
"""
import json
import shutil
from io import BufferedReader, BytesIO, StringIO, TextIOWrapper
from pathlib import Path
from typing import IO, Union


#  https://stackoverflow.com/questions/55889474/convert-io-stringio-to-io-bytesio
#  made by foobarna, improved by imporsen
class BytesIOWrapper(BufferedReader):
    """
    Wrap a buffered bytes stream over TextIOBase string stream.
    """

    def __init__(self, text_io_buffer, encoding=None, errors=None, **kwargs):
        super().__init__(text_io_buffer, **kwargs)
        self.encoding = encoding or text_io_buffer.encoding or "utf-8"
        self.errors = errors or text_io_buffer.errors or "strict"

    def _encoding_call(self, method_name, *args, **kwargs):
        raw_method = getattr(self.raw, method_name)
        val = raw_method(*args, **kwargs)
        return val.encode(self.encoding, errors=self.errors)

    def read(self, size=-1):
        return self._encoding_call("read", size)

    def read1(self, size=-1):
        return self._encoding_call("read1", size)

    def peek(self, size=-1):
        return self._encoding_call("peek", size)


def wrap_bytes(src: IO) -> StringIO:
    """
    Wrap a BytesIO in a StringIO.
    """
    if isinstance(src, BytesIO):
        return TextIOWrapper(src)
    return src


def wrap_string(src: IO) -> BytesIO:
    """
    Wrap a StringIO in a BytesIO.
    """
    if isinstance(src, StringIO):
        return BytesIOWrapper(src)
    return src


def write_stringio(src: str) -> StringIO:
    """
    Write string in TextStream StringIO.
    """
    stringio = StringIO()
    stringio.write(src)
    stringio.seek(0)
    return stringio


def write_bytesio(src: str) -> BytesIO:
    """
    Write string in ByteStream BytesIO.
    """
    bytesio = BytesIO()
    bytesio.write(src.encode())
    bytesio.seek(0)
    return bytesio


def write_json(data: dict, path: Union[str, Path]) -> None:
    """
    Store JSON file.
    """
    with open(path, "w") as file:
        json.dump(data, file)


def write_text(string: str, path: Union[str, Path]) -> None:
    """
    Write text on a file.
    """
    with open(path, "w") as file:
        file.write(string)


def write_bytes(byt: bytes, path: Union[str, Path]) -> None:
    """
    Write text on a file.
    """
    with open(path, "wb") as file:
        file.write(byt)


def write_object(buff: IO, dst: str) -> None:
    """
    Save a buffer as file.
    """
    buff.seek(0)
    write_mode = "wb" if isinstance(buff, BytesIO) else "w"
    with open(dst, write_mode) as file:
        shutil.copyfileobj(buff, file)
