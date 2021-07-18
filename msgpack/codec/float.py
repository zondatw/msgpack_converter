import struct

from msgpack.core.base import Payload

class Encoder:
    """Float Encoder
    
    Float format family stores a floating point number in 5 bytes or 9 bytes.

    float 32 stores a floating point number in IEEE 754 single precision floating point number format:
    +--------+--------+--------+--------+--------+
    |  0xca  |XXXXXXXX|XXXXXXXX|XXXXXXXX|XXXXXXXX|
    +--------+--------+--------+--------+--------+

    float 64 stores a floating point number in IEEE 754 double precision floating point number format:
    +--------+--------+--------+--------+--------+--------+--------+--------+--------+
    |  0xcb  |YYYYYYYY|YYYYYYYY|YYYYYYYY|YYYYYYYY|YYYYYYYY|YYYYYYYY|YYYYYYYY|YYYYYYYY|
    +--------+--------+--------+--------+--------+--------+--------+--------+--------+

    where
    * XXXXXXXX_XXXXXXXX_XXXXXXXX_XXXXXXXX is a big-endian IEEE 754 single precision floating point number.
    Extension of precision from single-precision to double-precision does not lose precision.
    * YYYYYYYY_YYYYYYYY_YYYYYYYY_YYYYYYYY_YYYYYYYY_YYYYYYYY_YYYYYYYY_YYYYYYYY is a big-endian
    IEEE 754 double precision floating point number
    """

    def __init__(self):
        self.payload = b""

    def get_header(self, value: float) -> bytes:
        if 1.2E-38 <= value <= 3.4E+38:
            return struct.pack(">B", 0xca)
        else: # Include NaN and Infinity
            return struct.pack(">B", 0xcb)

    def get_value(self, value: float) -> bytes:
        if 1.2E-38 <= value <= 3.4E+38:
            return struct.pack(">f", value)
        else: # Include NaN and Infinity
            return struct.pack(">d", value)

    def encode(self, value: float):
        self.payload = self.get_header(value) + self.get_value(value)

    def get_payload(self) -> bytes:
        return self.payload

class Decoder:
    """Float Decoder
    
    Float format family stores a floating point number in 5 bytes or 9 bytes.

    float 32 stores a floating point number in IEEE 754 single precision floating point number format:
    +--------+--------+--------+--------+--------+
    |  0xca  |XXXXXXXX|XXXXXXXX|XXXXXXXX|XXXXXXXX|
    +--------+--------+--------+--------+--------+

    float 64 stores a floating point number in IEEE 754 double precision floating point number format:
    +--------+--------+--------+--------+--------+--------+--------+--------+--------+
    |  0xcb  |YYYYYYYY|YYYYYYYY|YYYYYYYY|YYYYYYYY|YYYYYYYY|YYYYYYYY|YYYYYYYY|YYYYYYYY|
    +--------+--------+--------+--------+--------+--------+--------+--------+--------+

    where
    * XXXXXXXX_XXXXXXXX_XXXXXXXX_XXXXXXXX is a big-endian IEEE 754 single precision floating point number.
    Extension of precision from single-precision to double-precision does not lose precision.
    * YYYYYYYY_YYYYYYYY_YYYYYYYY_YYYYYYYY_YYYYYYYY_YYYYYYYY_YYYYYYYY_YYYYYYYY is a big-endian
    IEEE 754 double precision floating point number
    """

    def __init__(self):
        self.elem = None

    def decode(self, first_byte: bytes, payload: Payload):
        self.elem = None
        if first_byte == 0xca:
            self.elem = struct.unpack(">f", payload.bytes(4))[0]
        elif first_byte == 0xcb:
            self.elem = struct.unpack(">d", payload.bytes(8))[0]

    def get_elem(self) -> float:
        return self.elem
