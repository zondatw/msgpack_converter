import struct

from msgpack.core.base import Payload


class Encoder:
    """Bool Encoder

    Bool format family stores false or true in 1 byte.

    false:
    +--------+
    |  0xc2  |
    +--------+

    true:
    +--------+
    |  0xc3  |
    +--------+
    """

    def __init__(self):
        self.payload = b""

    def encode(self, value: bool):
        if value:
            self.payload = struct.pack("B", 0xc3)
        else:
            self.payload = struct.pack("B", 0xc2)

    def get_payload(self) -> bytes:
        return self.payload


class Decoder:
    """Bool Decoder

    Bool format family stores false or true in 1 byte.

    false:
    +--------+
    |  0xc2  |
    +--------+

    true:
    +--------+
    |  0xc3  |
    +--------+
    """

    def __init__(self):
        self.elem = None

    def decode(self, first_byte: bytes, payload: Payload):
        self.elem = None
        if first_byte == 0xc2:
            self.elem = False
        elif first_byte == 0xc3:
            self.elem = True

    def get_elem(self) -> bool:
        return self.elem
