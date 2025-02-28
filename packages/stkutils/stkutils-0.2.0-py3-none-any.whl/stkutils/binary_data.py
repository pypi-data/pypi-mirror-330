from typing import Any

# import struct
# from typing import Any
from perl_binary_packing import pack as _pack
from perl_binary_packing import unpack as _unpack

# Сопоставление форматов
# перла https://perldoc.perl.org/functions/pack
# и питона https://docs.python.org/3/library/struct.html


def unpack(format_str_full, data: bytes) -> list:
    return list(_unpack(format_str_full, data))


def pack(perl_format_str: str, *args: Any) -> bytes:
    return _pack(perl_format_str, *args)
