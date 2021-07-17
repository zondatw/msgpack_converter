import struct


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
