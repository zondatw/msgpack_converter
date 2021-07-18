import struct
from datetime import datetime, timezone, timedelta

from .ext import ExtStruct
from .ext import Encoder as ExtEncoder
from .ext import Decoder as ExtDecoder

TYPE = -1

class TimestampStruct(ExtStruct):
    def __init__(self, original_datetime: datetime = None, data: bytes = None, isEncodeMode=True):
        """TimestampStruct
        
        When isEncodeMode == True, arguments:
            original_datetime
        
        When isEncodeMode == False, it mean decode mode, arguments:
            data
        """

        if isEncodeMode:
            self.datetime = original_datetime
            self.seconds = int(self.datetime.timestamp())
            self.nanosec = self.datetime.microsecond * 1000
            if (self.seconds >> 34) == 0:
                if self.nanosec == 0:
                    data = struct.pack(">I", self.seconds)
                else:
                    data = struct.pack(">Q", (self.nanosec << 34) | self.seconds)
            else:
                data = struct.pack(">Iq", self.nanosec, self.seconds)
        else:
            if len(data) == 4:
                self.seconds = struct.unpack(">I", data)[0]
                self.nanosec = 0
            elif len(data) == 8:
                total_timestamp = struct.unpack(">Q", data)[0]
                self.seconds = total_timestamp & 0x00000003ffffffff
                self.nanosec = total_timestamp >> 34
            elif len(data) == 12:
                (self.nanosec, self.seconds) = struct.unpack(">Iq", data)

            self.datetime = datetime(1970, 1, 1, 0, 0, 0, 0, tzinfo=timezone.utc) + timedelta(seconds=self.seconds)
            self.datetime = self.datetime.replace(microsecond=self.nanosec // 1000)
        super().__init__(TYPE, data)
        self.custom_attribute_list.extend(["datetime", "seconds", "nanosec"])

    def __repr__(self) -> str:
        return self.datetime.strftime("%Y/%m/%d %H:%M:%S.%f%z")


def decode_struct(data: bytes):
    return TimestampStruct(data=data, isEncodeMode=False)

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
    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
        self.register_ext(TYPE, decode_struct)