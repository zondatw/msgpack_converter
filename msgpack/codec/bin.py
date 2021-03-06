import struct

from msgpack.core.base import Payload
from msgpack.core.limitations import MAX_BIN_OBJ_LEN
from msgpack.core.exceptions import BinOutOfRange


class Encoder:
    """Bin Encoder
    
    Bin format family stores an byte array in 2, 3, or 5 bytes of extra bytes in addition to the size of the byte array.

    bin 8 stores a byte array whose length is upto (2^8)-1 bytes:
    +--------+--------+========+
    |  0xc4  |XXXXXXXX|  data  |
    +--------+--------+========+

    bin 16 stores a byte array whose length is upto (2^16)-1 bytes:
    +--------+--------+--------+========+
    |  0xc5  |YYYYYYYY|YYYYYYYY|  data  |
    +--------+--------+--------+========+

    bin 32 stores a byte array whose length is upto (2^32)-1 bytes:
    +--------+--------+--------+--------+--------+========+
    |  0xc6  |ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|  data  |
    +--------+--------+--------+--------+--------+========+

    where
    * XXXXXXXX is a 8-bit unsigned integer which represents N
    * YYYYYYYY_YYYYYYYY is a 16-bit big-endian unsigned integer which represents N
    * ZZZZZZZZ_ZZZZZZZZ_ZZZZZZZZ_ZZZZZZZZ is a 32-bit big-endian unsigned integer which represents N
    * N is the length of data
    """

    def __init__(self):
        self.payload = b""

    def get_header(self, length: int) -> bytes:
        if length <= ((2 ** 8) - 1):
            return struct.pack(">BB", 0xc4, length)
        elif length <= ((2 ** 16) - 1):
            return struct.pack(">BH", 0xc5, length)
        else:
            return struct.pack(">BI", 0xc6, length)

    def encode(self, value: bytes) -> bytes:
        length = len(value)
        if length > MAX_BIN_OBJ_LEN:
            raise BinOutOfRange(length)

        self.payload = self.get_header(length) + struct.pack(f"{length}s", value)

    def get_payload(self) -> bytes:
        return self.payload


class Decoder:
    """Bin Decoder
    
    Bin format family stores an byte array in 2, 3, or 5 bytes of extra bytes in addition to the size of the byte array.

    bin 8 stores a byte array whose length is upto (2^8)-1 bytes:
    +--------+--------+========+
    |  0xc4  |XXXXXXXX|  data  |
    +--------+--------+========+

    bin 16 stores a byte array whose length is upto (2^16)-1 bytes:
    +--------+--------+--------+========+
    |  0xc5  |YYYYYYYY|YYYYYYYY|  data  |
    +--------+--------+--------+========+

    bin 32 stores a byte array whose length is upto (2^32)-1 bytes:
    +--------+--------+--------+--------+--------+========+
    |  0xc6  |ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|  data  |
    +--------+--------+--------+--------+--------+========+

    where
    * XXXXXXXX is a 8-bit unsigned integer which represents N
    * YYYYYYYY_YYYYYYYY is a 16-bit big-endian unsigned integer which represents N
    * ZZZZZZZZ_ZZZZZZZZ_ZZZZZZZZ_ZZZZZZZZ is a 32-bit big-endian unsigned integer which represents N
    * N is the length of data
    """

    def __init__(self):
        self.elem = b""

    def get_length(self, first_byte: bytes, payload: Payload) -> int:
        if first_byte == 0xc4:
            length = struct.unpack(">B", payload.bytes(1))[0]
        elif first_byte == 0xc5:
            length = struct.unpack(">H", payload.bytes(2))[0]
        elif first_byte == 0xc6:
            length = struct.unpack(">I", payload.bytes(4))[0]
        return length

    def decode(self, first_byte: bytes, payload: Payload):
        self.elem = b""
        length = self.get_length(first_byte, payload)
        if length > MAX_BIN_OBJ_LEN:
            raise BinOutOfRange(length)

        self.elem += payload.bytes(length)

    def get_elem(self) -> bytes:
        return self.elem