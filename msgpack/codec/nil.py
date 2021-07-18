import struct

from msgpack.core.base import Payload

class Encoder:
    """Nil Encoder

    Nil format stores nil in 1 byte.

    nil:
    +--------+
    |  0xc0  |
    +--------+
    """

    def __init__(self):
        self.payload = struct.pack("B", 0xc0)

    def encode(self, value: None):
        pass

    def get_payload(self) -> bytes:
        return self.payload

class Decoder:
    """Nil Decoder

    Nil format stores nil in 1 byte.

    nil:
    +--------+
    |  0xc0  |
    +--------+
    """

    def __init__(self):
        self.elem = None

    def decode(self, first_byte: bytes, payload: Payload):
        pass

    def get_elem(self) -> None:
        return self.elem
