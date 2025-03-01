from __future__ import annotations

import base64
import struct
import zlib
from functools import reduce
from operator import mul
from typing import Any, Callable

from pysll.exceptions import UnknownTokenError
from pysll.feature_flags import FeatureFlags


def decode(compressed: str) -> str:
    """The encoded data in a compressed field is a zlib compression of a base64
    encoded string prepended with `1.` that serializes a MM expression.

    See
    https://mathematica.stackexchange.com/questions/104660/what-algorithm-do-the-compress-and-uncompress-functions-use
    for more info
    """
    return _decode(zlib.decompress(base64.b64decode(compressed[2:])))


def _decode(data: bytes) -> str:
    """Decodes the MM binary object representation into a MM expression.

    See
    https://mathematica.stackexchange.com/questions/104660/what-algorithm-do-the-compress-and-uncompress-functions-use
    for more info
    """
    expressions: list[str] = []
    while data:
        expression, data = decode_token(data)
        expressions.append(expression)

    return "".join(map(str, expressions))


def decode_token(data: bytes) -> tuple[Any, bytes]:
    """Parse a single token from the binary object representation."""

    # First, check if we're seeing the header
    if data[:4] == b"!boR":
        # Just strip the header
        return "", data[4:]

    if not data:
        return "", b""

    # If not, then check if we can read the leading character to determine the token type
    token, data = data[0], data[1:]
    match token:
        case 105:  # b"i"
            return _decode_integer(data)
        case 114:  # b"r"
            return _decode_real(data)
        case 83 | 115 | 73:  # b"S", b"s", b"I"
            # Strings, symbols, large integers
            return _decode_string(data)
        case 102:  # b"f"
            return _decode_expression(data)
        case 101:  # b"e"
            return _decode_tensor(data)
        case 82:  # b"R"
            # this should be parsable as a string which produces something like '123.123`1.12'
            # we will get the numeric string, and split out the first value, convert it to
            # a float and return. we will ignore the precision info b/c python doesn't care
            value, rest = _decode_string(data)
            if not isinstance(value, str):
                raise ValueError(f"Expected an arbitrary precision real string, and got {type(value)}")
            real, _ = value.split("`")

            return float(real), rest
        case _:
            raise UnknownTokenError(token, data)


def _decode_integer(data: bytes):
    return struct.unpack("<i", data[:4])[0], data[4:]


def _decode_real(data: bytes):
    return struct.unpack("<d", data[:8])[0], data[8:]


def _decode_string(data: bytes):
    # the first four bytes hold the size of the string
    size, data = _decode_integer(data)
    return data[:size].decode("utf-8"), data[size:]


def _decode_expression(data: bytes):
    # Integer tells us the expression size
    size, data = _decode_integer(data)

    # Next, we got the symbol head
    (
        head,
        data,
    ) = decode_token(data)

    # Finally, arguments.
    arguments = []
    for _ in range(size):
        if not data:
            break

        argument, data = decode_token(data)
        arguments.append(argument)

    return f"{head}[{', '.join(map(str, arguments))}]", data


def _decode_tensor(
    data: bytes,
    decoder: Callable[[bytes], tuple[Any, bytes]] | None = None,
):
    dimensions, data = _decode_integer(data)

    shapes = []
    for _ in range(dimensions):
        size, data = _decode_integer(data)
        shapes.append(size)

    if FeatureFlags.from_environment().use_numpy:
        import numpy as np  # type:ignore (run pip install pysll[numpy])

        n = reduce(mul, shapes) * 8
        return np.frombuffer(data[:n], dtype=np.float64).reshape(*shapes).tolist(), data[n:]

    return _reshape(tuple(shapes), data, decoder or _decode_real)


def _reshape(
    shapes: tuple[int, ...],
    data: bytes,
    decoder: Callable[[bytes], tuple[Any, bytes]],
) -> tuple[list, bytes]:
    if not shapes:
        return decoder(data)

    tensor = []
    head, *tail = shapes
    for _ in range(head):
        vector, data = _reshape(tuple(tail), data, decoder)
        tensor.append(vector)

    return tensor, data
