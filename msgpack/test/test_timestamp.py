import struct
from datetime import datetime

from msgpack.codec.timestamp import Encoder as TimestampEncoder
from msgpack.codec.timestamp import TimestampStruct


class TestStruct:
    def test_32(self):
        test_ext = TimestampStruct(datetime.strptime("1970-01-02 00:00:00.000000+0000", "%Y-%m-%d %H:%M:%S.%f%z"))
        assert test_ext.data == b'\x00\x01\x51\x80'

        test_ext = TimestampStruct(datetime.strptime("2106-02-07 06:28:15.000000+0000", "%Y-%m-%d %H:%M:%S.%f%z"))
        assert test_ext.data == b'\xff\xff\xff\xff'

    def test_64(self):
        test_ext = TimestampStruct(datetime.strptime("1970-01-02 00:00:00.000001+0000", "%Y-%m-%d %H:%M:%S.%f%z"))
        assert test_ext.data == b'\x00\x00\x0f\xa0\x00\x01\x51\x80'

        test_ext = TimestampStruct(datetime.strptime("2514-05-30 01:53:03.999999+0000", "%Y-%m-%d %H:%M:%S.%f%z"))
        assert test_ext.data == b'\xeek\x18c\xff\xff\xff\xff'

    def test_96(self):
        test_ext = TimestampStruct(datetime.strptime("0001-01-01 00:00:00.000001+0000", "%Y-%m-%d %H:%M:%S.%f%z"))
        assert test_ext.data == b'\x00\x00\x03\xe8\xff\xff\xff\xf1\x88\x6e\x09\x00'

        test_ext = TimestampStruct(datetime.strptime("9999-12-31 23:59:59.999999+0000", "%Y-%m-%d %H:%M:%S.%f%z"))
        assert test_ext.data == b'\x3b\x9a\xc6\x18\x00\x00\x00\x3a\xff\xf4\x41\x80'

class TestEncode:
    @classmethod
    def setup_class(cls):
        cls.encoder = TimestampEncoder()

    def test_32(self):
        # Min
        # Different OS have different minimum datetime, current test writes on Windows 10
        test_ext = TimestampStruct(datetime.strptime("1970-01-02 00:00:00.000000+0000", "%Y-%m-%d %H:%M:%S.%f%z"))
        self.encoder.encode(test_ext)
        length = len(test_ext.data)
        assert self.encoder.get_payload() == (
            struct.pack(">Bb", 0xd6, test_ext.type) + struct.pack(f"{length}s", test_ext.data)
        )

        # Max
        test_ext = TimestampStruct(datetime.strptime("2106-02-07 06:28:15.000000+0000", "%Y-%m-%d %H:%M:%S.%f%z"))
        self.encoder.encode(test_ext)
        length = len(test_ext.data)
        assert self.encoder.get_payload() == (
            struct.pack(">Bb", 0xd6, test_ext.type) + struct.pack(f"{length}s", test_ext.data)
        )

    def test_64(self):
        # Min
        # Different OS have different minimum datetime, current test writes on Windows 10
        test_ext = TimestampStruct(datetime.strptime("1970-01-02 00:00:00.000001+0000", "%Y-%m-%d %H:%M:%S.%f%z"))
        self.encoder.encode(test_ext)
        length = len(test_ext.data)
        assert self.encoder.get_payload() == (
            struct.pack(">Bb", 0xd7, test_ext.type) + struct.pack(f"{length}s", test_ext.data)
        )

        # Max
        test_ext = TimestampStruct(datetime.strptime("2514-05-30 01:53:03.999999+0000", "%Y-%m-%d %H:%M:%S.%f%z"))
        self.encoder.encode(test_ext)
        length = len(test_ext.data)
        assert self.encoder.get_payload() == (
            struct.pack(">Bb", 0xd7, test_ext.type) + struct.pack(f"{length}s", test_ext.data)
        )

    def test_96(self):
        # Min
        # min supported -292277022657-01-27 08:29:52, but min year of python datetime is 0001
        test_ext = TimestampStruct(datetime.strptime("0001-01-01 00:00:00.000001+0000", "%Y-%m-%d %H:%M:%S.%f%z"))
        self.encoder.encode(test_ext)
        length = len(test_ext.data)
        assert self.encoder.get_payload() == (
            struct.pack(">BBb", 0xc7, 12, test_ext.type) + struct.pack(f"{length}s", test_ext.data)
        )

        # Max
        # min supported 292277026596-12-04 15:30:08.000000000, but max year of python datetime is 9999
        test_ext = TimestampStruct(datetime.strptime("9999-12-31 23:59:59.999999+0000", "%Y-%m-%d %H:%M:%S.%f%z"))
        self.encoder.encode(test_ext)
        length = len(test_ext.data)
        assert self.encoder.get_payload() == (
            struct.pack(">BBb", 0xc7, 12, test_ext.type) + struct.pack(f"{length}s", test_ext.data)
        )
