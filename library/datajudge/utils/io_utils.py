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
        super(BytesIOWrapper, self).__init__(text_io_buffer, **kwargs)
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
    src.seek(0)
    return TextIOWrapper(src)


def wrap_string(src: IO) -> BytesIO:
    src.seek(0)
    if isinstance(src, StringIO):
        src = BytesIOWrapper(src)
    return src
