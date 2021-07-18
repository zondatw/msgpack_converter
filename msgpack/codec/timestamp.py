import struct
from datetime import datetime

from msgpack.core.base import Payload
from .ext import ExtStruct
from .ext import Encoder as ExtEncoder
from .ext import Decoder as ExtDecoder


class TimestampStruct(ExtStruct):
    def __init__(self, t: datetime):
        type = -1
        self.datetime = t
        self.seconds = int(self.datetime.timestamp())
        self.nanosec = self.datetime.microsecond * 1000
        if (self.seconds >> 34) == 0:
            if self.nanosec == 0:
                data = struct.pack(">I", self.seconds)
            else:
                data = struct.pack(">Q", (self.nanosec << 34) | self.seconds)
        else:
            data = struct.pack(">Iq", self.nanosec, self.seconds)

        super().__init__(type, data)
        self.custom_attribute_list.extend(["datetime", "seconds", "nanosec"])


class Encoder(ExtEncoder):
    """Timestamp Encoder

    Timestamp extension type is assigned to extension type -1. It defines 3 formats: 32-bit format, 64-bit format, and 96-bit format.

    timestamp 32 stores the number of seconds that have elapsed since 1970-01-01 00:00:00 UTC
    in an 32-bit unsigned integer:
    +--------+--------+--------+--------+--------+--------+
    |  0xd6  |   -1   |   seconds in 32-bit unsigned int  |
    +--------+--------+--------+--------+--------+--------+

    timestamp 64 stores the number of seconds and nanoseconds that have elapsed since 1970-01-01 00:00:00 UTC
    in 32-bit unsigned integers:
    +--------+--------+--------+--------+--------+------|-+--------+--------+--------+--------+
    |  0xd7  |   -1   | nanosec. in 30-bit unsigned int |   seconds in 34-bit unsigned int    |
    +--------+--------+--------+--------+--------+------^-+--------+--------+--------+--------+

    timestamp 96 stores the number of seconds and nanoseconds that have elapsed since 1970-01-01 00:00:00 UTC
    in 64-bit signed integer and 32-bit unsigned integer:
    +--------+--------+--------+--------+--------+--------+--------+
    |  0xc7  |   12   |   -1   |nanoseconds in 32-bit unsigned int |
    +--------+--------+--------+--------+--------+--------+--------+
    +--------+--------+--------+--------+--------+--------+--------+--------+
                        seconds in 64-bit signed int                        |
    +--------+--------+--------+--------+--------+--------+--------+--------+
    """
    pass


class Decoder(ExtDecoder):
    """Timestamp Decoder

    Timestamp extension type is assigned to extension type -1. It defines 3 formats: 32-bit format, 64-bit format, and 96-bit format.

    timestamp 32 stores the number of seconds that have elapsed since 1970-01-01 00:00:00 UTC
    in an 32-bit unsigned integer:
    +--------+--------+--------+--------+--------+--------+
    |  0xd6  |   -1   |   seconds in 32-bit unsigned int  |
    +--------+--------+--------+--------+--------+--------+

    timestamp 64 stores the number of seconds and nanoseconds that have elapsed since 1970-01-01 00:00:00 UTC
    in 32-bit unsigned integers:
    +--------+--------+--------+--------+--------+------|-+--------+--------+--------+--------+
    |  0xd7  |   -1   | nanosec. in 30-bit unsigned int |   seconds in 34-bit unsigned int    |
    +--------+--------+--------+--------+--------+------^-+--------+--------+--------+--------+

    timestamp 96 stores the number of seconds and nanoseconds that have elapsed since 1970-01-01 00:00:00 UTC
    in 64-bit signed integer and 32-bit unsigned integer:
    +--------+--------+--------+--------+--------+--------+--------+
    |  0xc7  |   12   |   -1   |nanoseconds in 32-bit unsigned int |
    +--------+--------+--------+--------+--------+--------+--------+
    +--------+--------+--------+--------+--------+--------+--------+--------+
                        seconds in 64-bit signed int                        |
    +--------+--------+--------+--------+--------+--------+--------+--------+
    """
    pass