import struct
from typing import List, Union, Dict

from msgpack.core.limitations import MAX_ARRAY_ELEM_NUM
from msgpack.core.exceptions import ArrayOutOfRange


class Encoder:
    """Array Encoder

    Array format family stores a sequence of elements in 1, 3, or 5 bytes of extra bytes in addition to the elements.

    fixarray stores an array whose length is upto 15 elements:
    +--------+~~~~~~~~~~~~~~~~~+
    |1001XXXX|    N objects    |
    +--------+~~~~~~~~~~~~~~~~~+

    array 16 stores an array whose length is upto (2^16)-1 elements:
    +--------+--------+--------+~~~~~~~~~~~~~~~~~+
    |  0xdc  |YYYYYYYY|YYYYYYYY|    N objects    |
    +--------+--------+--------+~~~~~~~~~~~~~~~~~+

    array 32 stores an array whose length is upto (2^32)-1 elements:
    +--------+--------+--------+--------+--------+~~~~~~~~~~~~~~~~~+
    |  0xdd  |ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|    N objects    |
    +--------+--------+--------+--------+--------+~~~~~~~~~~~~~~~~~+

    where
    * XXXX is a 4-bit unsigned integer which represents N
    * YYYYYYYY_YYYYYYYY is a 16-bit big-endian unsigned integer which represents N
    * ZZZZZZZZ_ZZZZZZZZ_ZZZZZZZZ_ZZZZZZZZ is a 32-bit big-endian unsigned integer which represents N
    * N is the size of an array
    """

    def __init__(self):
        self.payload = b""

    def get_header(self, length: int) -> bytes:
        if length <= 15:
            base = int("10010000", 2)
            return struct.pack("B", base + length)
        elif length <= ((2 ** 16) - 1):
            return struct.pack(">BH", 0xdc, length)
        else:
            return struct.pack(">BI", 0xdd, length)

    def encode(self, array: List) -> Union[int, str, bytes, Dict, List, bool, None,]:
        length = len(array)
        if length > MAX_ARRAY_ELEM_NUM:
            raise ArrayOutOfRange(length)

        self.payload = self.get_header(length)

        for item in array:
            self.payload += (yield item)
            yield # for send

    def get_payload(self) -> bytes:
        return self.payload
