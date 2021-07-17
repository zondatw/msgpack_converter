import struct

from msgpack.core.limitations import MAX_STR_OBJ_SIZE
from msgpack.core.exceptions import StrOutOfRange


class Encoder:
    """Str Encoder
    
    Str format family stores a byte array in 1, 2, 3, or 5 bytes of extra bytes in addition to the size of the byte array.

    fixstr stores a byte array whose length is upto 31 bytes:
    +--------+========+
    |101XXXXX|  data  |
    +--------+========+

    str 8 stores a byte array whose length is upto (2^8)-1 bytes:
    +--------+--------+========+
    |  0xd9  |YYYYYYYY|  data  |
    +--------+--------+========+

    str 16 stores a byte array whose length is upto (2^16)-1 bytes:
    +--------+--------+--------+========+
    |  0xda  |ZZZZZZZZ|ZZZZZZZZ|  data  |
    +--------+--------+--------+========+

    str 32 stores a byte array whose length is upto (2^32)-1 bytes:
    +--------+--------+--------+--------+--------+========+
    |  0xdb  |AAAAAAAA|AAAAAAAA|AAAAAAAA|AAAAAAAA|  data  |
    +--------+--------+--------+--------+--------+========+

    where
    * XXXXX is a 5-bit unsigned integer which represents N
    * YYYYYYYY is a 8-bit unsigned integer which represents N
    * ZZZZZZZZ_ZZZZZZZZ is a 16-bit big-endian unsigned integer which represents N
    * AAAAAAAA_AAAAAAAA_AAAAAAAA_AAAAAAAA is a 32-bit big-endian unsigned integer which represents N
    * N is the length of data
    """

    def __init__(self):
        self.payload = b""

    def get_header(self, length: int) -> bytes:
        if length <= 31:
            base = int("10100000", 2)
            return struct.pack("B", base + length)
        elif length <= ((2 ** 8) - 1):
            return struct.pack(">BB", 0xd9, length)
        elif length <= ((2 ** 16) - 1):
            return struct.pack(">BH", 0xda, length)
        else:
            return struct.pack(">BI", 0xdb, length)

    def encode(self, value: str):
        value = value.encode("utf-8")
        length = len(value)
        if length > MAX_STR_OBJ_SIZE:
            raise StrOutOfRange(length)

        self.payload = self.get_header(length) + struct.pack(f"{length}s", value)

    def get_payload(self) -> bytes:
        return self.payload
