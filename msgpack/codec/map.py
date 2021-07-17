import struct
from typing import Dict, Tuple

from msgpack.core.limitations import MAX_MAP_KV_NUM
from msgpack.core.exceptions import MapOutOfRange


class Encoder:
    """MAP Encoder

    Map format family stores a sequence of key-value pairs in 1, 3, or 5 bytes of extra bytes in addition to the key-value pairs.

    fixmap stores a map whose length is upto 15 elements
    +--------+~~~~~~~~~~~~~~~~~+
    |1000XXXX|   N*2 objects   |
    +--------+~~~~~~~~~~~~~~~~~+

    map 16 stores a map whose length is upto (2^16)-1 elements
    +--------+--------+--------+~~~~~~~~~~~~~~~~~+
    |  0xde  |YYYYYYYY|YYYYYYYY|   N*2 objects   |
    +--------+--------+--------+~~~~~~~~~~~~~~~~~+

    map 32 stores a map whose length is upto (2^32)-1 elements
    +--------+--------+--------+--------+--------+~~~~~~~~~~~~~~~~~+
    |  0xdf  |ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|ZZZZZZZZ|   N*2 objects   |
    +--------+--------+--------+--------+--------+~~~~~~~~~~~~~~~~~+

    where
    * XXXX is a 4-bit unsigned integer which represents N
    * YYYYYYYY_YYYYYYYY is a 16-bit big-endian unsigned integer which represents N
    * ZZZZZZZZ_ZZZZZZZZ_ZZZZZZZZ_ZZZZZZZZ is a 32-bit big-endian unsigned integer which represents N
    * N is the size of a map
    * odd elements in objects are keys of a map
    * the next element of a key is its associated value
    """

    def __init__(self):
        self.payload = b""

    def get_header(self, key_number: int) -> bytes:
        if key_number <= 15:
            base = int("10000000", 2)
            return struct.pack("B", base + key_number)
        elif key_number <= ((2 ** 16) - 1):
            return struct.pack(">BH", 0xde, key_number)
        else:
            return struct.pack(">BI", 0xdf, key_number)

    def encode(self, json_data: Dict) -> Tuple:
        key_number = len(json_data.keys())
        if key_number > MAX_MAP_KV_NUM:
            raise MapOutOfRange(key_number)

        self.payload = self.get_header(key_number)

        for key, value in json_data.items():
            self.payload += (yield (key, value))
            yield # for send

    def get_payload(self) -> bytes:
        return self.payload
