"""
Common IO utils.
"""
from io import BufferedReader, BytesIO, StringIO, TextIOWrapper
from typing import IO


#  https://stackoverflow.com/questions/55889474/convert-io-stringio-to-io-bytesio
#  made by foobarna, improved by imporsen
class BytesIOWrapper(BufferedReader):
    """
    Wrap a buffered bytes stream over TextIOBase string stream.
    """

    def __init__(self, text_io_buffer, encoding=None, errors=None, **kwargs):
        super().__init__(text_io_buffer, **kwargs)
        self.encoding = encoding or text_io_buffer.encoding or 'utf-8'
        self.errors = errors or text_io_buffer.errors or 'strict'

    def _encoding_call(self, method_name, *args, **kwargs):
        raw_method = getattr(self.raw, method_name)
        val = raw_method(*args, **kwargs)
        return val.encode(self.encoding, errors=self.errors)

    def read(self, size=-1):
        return self._encoding_call('read', size)

    def read1(self, size=-1):
        return self._encoding_call('read1', size)

    def peek(self, size=-1):
        return self._encoding_call('peek', size)


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
