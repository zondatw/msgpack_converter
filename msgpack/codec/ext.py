import struct

from msgpack.core.limitations import MIN_EXT_TYPE, MAX_EXT_TYPE, MIN_EXT_DATA_LEN, MAX_EXT_DATA_LEN
from msgpack.core.exceptions import ExtTypeOutOfRange, ExtDataOutOfRange


class ExtStruct:
    def __init__(self, type: int, data: bytes):
        if not (MIN_EXT_TYPE <= type <= MAX_EXT_TYPE):
            raise ExtTypeOutOfRange(type)

        if not (MIN_EXT_DATA_LEN <= len(data) <= MAX_EXT_DATA_LEN):
            raise ExtDataOutOfRange(len(data))

        self.type = type
        self.data = data


class Encoder:
    """Ext Encoder

    Ext format family stores a tuple of an integer and a byte array.

    type:
        [0, 127]: application-specific types
        [-128, -1]: reserved for predefined types

    fixext 1 stores an integer and a byte array whose length is 1 byte
    +--------+--------+--------+
    |  0xd4  |  type  |  data  |
    +--------+--------+--------+

    fixext 2 stores an integer and a byte array whose length is 2 bytes
    +--------+--------+--------+--------+
    |  0xd5  |  type  |       data      |
    +--------+--------+--------+--------+

    fixext 4 stores an integer and a byte array whose length is 4 bytes
    +--------+--------+--------+--------+--------+--------+
    |  0xd6  |  type  |                data               |
    +--------+--------+--------+--------+--------+--------+

    fixext 8 stores an integer and a byte array whose length is 8 bytes
    +--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
    |  0xd7  |  type  |                                  data                                 |
    +--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+

    fixext 16 stores an integer and a byte array whose length is 16 bytes
    +--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
    |  0xd8  |  type  |                                  data                                  
    +--------+--------+--------+--------+--------+--------+--------+--------+--------+--------+
    +--------+--------+--------+--------+--------+--------+--------+--------+
                                data (cont.)                              |
    +--------+--------+--------+--------+--------+--------+--------+--------+

    ext 8 stores an integer and a byte array whose length is upto (2^8)-1 bytes:
    +--------+--------+--------+========+
    |  0xc7  |XXXXXXXX|  type  |  data  |
    +--------+--------+--------+========+

    ext 16 stores an integer and a byte array whose length is upto (2^16)-1 bytes:
    +--------+--------+--------+--------+========+
    |  0xc8  |YYYYYYYY|YYYYYYYY|  type  |  data  |
    +--------+--------+--------+--------+========+

    ext 32 stores an integer and a byte array whose length is upto (2^32)-1 bytes:
    +--------+--------+--------+--------+--------+--------+========+
    |  0xc9  |ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|  type  |  data  |
    +--------+--------+--------+--------+--------+--------+========+

    where
    * XXXXXXXX is a 8-bit unsigned integer which represents N
    * YYYYYYYY_YYYYYYYY is a 16-bit big-endian unsigned integer which represents N
    * ZZZZZZZZ_ZZZZZZZZ_ZZZZZZZZ_ZZZZZZZZ is a big-endian 32-bit unsigned integer which represents N
    * N is a length of data
    * type is a signed 8-bit signed integer
    * type < 0 is reserved for future extension including 2-byte type information
    """

    def __init__(self):
        self.payload = b""

    def get_header(self, length: int, type: int) -> bytes:
        if length == 1:
            return struct.pack(">Bb", 0xd4, type)
        elif length == 2:
            return struct.pack(">Bb", 0xd5, type)
        elif length == 4:
            return struct.pack(">Bb", 0xd6, type)
        elif length == 8:
            return struct.pack(">Bb", 0xd7, type)
        elif length == 16:
            return struct.pack(">Bb", 0xd8, type)
        elif length <= ((2 ** 8) - 1):
            return struct.pack(">BBb", 0xc7, length, type)
        elif length <= ((2 ** 16) - 1):
            return struct.pack(">BHb", 0xc8, length, type)
        elif length <= ((2 ** 32) - 1):
            return struct.pack(">BIb", 0xc9, length, type)

    def encode(self, ext_struct: ExtStruct):
        length = len(ext_struct.data)
        self.payload = self.get_header(length, ext_struct.type) + struct.pack(f"{length}s", ext_struct.data)

    def get_payload(self) -> bytes:
        return self.payload
