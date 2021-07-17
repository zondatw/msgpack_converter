import struct

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

    def get_value(self, value: float):
        if 1.2E-38 <= value <= 3.4E+38:
            return struct.pack(">f", value)
        else: # Include NaN and Infinity
            return struct.pack(">d", value)

    def encode(self, value: float):
        self.payload = self.get_header(value) + self.get_value(value)

    def get_payload(self) -> bytes:
        return self.payload
