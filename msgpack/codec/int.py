import struct

from msgpack.core.limitations import MIN_INT_OBJ_VALUE, MAX_INT_OBJ_VALUE
from msgpack.core.exceptions import IntOutOfRange


class Encoder:
    """Int Encoder
    
    Int format family stores an integer in 1, 2, 3, 5, or 9 bytes.

    positive fixint stores 7-bit positive integer
    +--------+
    |0XXXXXXX|
    +--------+

    negative fixint stores 5-bit negative integer
    +--------+
    |111YYYYY|
    +--------+

    * 0XXXXXXX is 8-bit unsigned integer
    * 111YYYYY is 8-bit signed integer

    uint 8 stores a 8-bit unsigned integer
    +--------+--------+
    |  0xcc  |ZZZZZZZZ|
    +--------+--------+

    uint 16 stores a 16-bit big-endian unsigned integer
    +--------+--------+--------+
    |  0xcd  |ZZZZZZZZ|ZZZZZZZZ|
    +--------+--------+--------+

    uint 32 stores a 32-bit big-endian unsigned integer
    +--------+--------+--------+--------+--------+
    |  0xce  |ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|
    +--------+--------+--------+--------+--------+

    uint 64 stores a 64-bit big-endian unsigned integer
    +--------+--------+--------+--------+--------+--------+--------+--------+--------+
    |  0xcf  |ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|
    +--------+--------+--------+--------+--------+--------+--------+--------+--------+

    int 8 stores a 8-bit signed integer
    +--------+--------+
    |  0xd0  |ZZZZZZZZ|
    +--------+--------+

    int 16 stores a 16-bit big-endian signed integer
    +--------+--------+--------+
    |  0xd1  |ZZZZZZZZ|ZZZZZZZZ|
    +--------+--------+--------+

    int 32 stores a 32-bit big-endian signed integer
    +--------+--------+--------+--------+--------+
    |  0xd2  |ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|
    +--------+--------+--------+--------+--------+

    int 64 stores a 64-bit big-endian signed integer
    +--------+--------+--------+--------+--------+--------+--------+--------+--------+
    |  0xd3  |ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|
    +--------+--------+--------+--------+--------+--------+--------+--------+--------+
    """

    def __init__(self):
        self.payload = b""

    def get_header(self, value: int) -> bytes:
        if 0 <= value <= 0x7f:
            return b""
        elif -32 <= value < 0:
            return b""
        elif -128 <= value <= 127:
            return struct.pack(">B", 0xd0)
        elif 0 <= value <= 255:
            return struct.pack(">B", 0xcc)
        elif -32768 <= value <= 32767:
            return struct.pack(">B", 0xd1)
        elif 0 <= value <= 65535:
            return struct.pack(">B", 0xcd)
        elif -2147483648 <= value <= 2147483647:
            return struct.pack(">B", 0xd2)
        elif 0 <= value <= 4294967295:
            return struct.pack(">B", 0xce)
        elif -9223372036854775808 <= value <= 9223372036854775807:
            return struct.pack(">B", 0xd3)
        elif 0 <= value <= 18446744073709551615:
            return struct.pack(">B", 0xcf)

    def get_value(self, value: int) -> bytes:
        if 0 <= value <= 0x7f:
            return struct.pack(">B", value)
        elif -32 <= value < 0:
            return struct.pack(">b", value)
        elif -128 <= value <= 127:
            return struct.pack(">b", value)
        elif 0 <= value <= 255:
            return struct.pack(">B", value)
        elif -32768 <= value <= 32767:
            return struct.pack(">h", value)
        elif 0 <= value <= 65535:
            return struct.pack(">H", value)
        elif -2147483648 <= value <= 2147483647:
            return struct.pack(">i", value)
        elif 0 <= value <= 4294967295:
            return struct.pack(">I", value)
        elif -9223372036854775808 <= value <= 9223372036854775807:
            return struct.pack(">q", value)
        elif 0 <= value <= 18446744073709551615:
            return struct.pack(">Q", value)

    def encode(self, value: int):
        if not (MIN_INT_OBJ_VALUE <= value <= MAX_INT_OBJ_VALUE):
            raise IntOutOfRange(value)

        self.payload = self.get_header(value) + self.get_value(value)

    def get_payload(self) -> bytes:
        return self.payload
