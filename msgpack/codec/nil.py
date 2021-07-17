import struct


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
