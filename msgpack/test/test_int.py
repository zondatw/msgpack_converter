import struct

import pytest

from msgpack.core.base import Payload
from msgpack.codec.int import Encoder as IntEncoder
from msgpack.codec.int import Decoder as IntDecoder

class TestEncode:
    @classmethod
    def setup_class(cls):
        cls.encoder = IntEncoder()

    def test_fixint_positive(self):
        # Min
        test_int = 0
        self.encoder.encode(test_int)
        assert self.encoder.get_payload() == (
            struct.pack(">B", test_int)
        )

        # Max
        test_int = 0x7f
        self.encoder.encode(test_int)
        assert self.encoder.get_payload() == (
            struct.pack(">B", test_int)
        )

    def test_fixint_negative(self):
        # Min
        test_int = -32
        self.encoder.encode(test_int)
        assert self.encoder.get_payload() == (
            struct.pack(">b", test_int)
        )

        # Max
        test_int = -1
        self.encoder.encode(test_int)
        assert self.encoder.get_payload() == (
            struct.pack(">b", test_int)
        )

    def test_uint_8(self):
        # Min
        test_int = -128
        self.encoder.encode(test_int)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xd0) + struct.pack(">b", test_int)
        )

        # Max
        test_int = -33
        self.encoder.encode(test_int)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xd0) + struct.pack(">b", test_int)
        )

    def test_int_8(self):
        # Min
        test_int = 128
        self.encoder.encode(test_int)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xcc) + struct.pack(">B", test_int)
        )

        # Max
        test_int = 255
        self.encoder.encode(test_int)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xcc) + struct.pack(">B", test_int)
        )

    def test_uint_16(self):
        # Min
        test_int = -32768
        self.encoder.encode(test_int)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xd1) + struct.pack(">h", test_int)
        )

        # Max
        test_int = 32767
        self.encoder.encode(test_int)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xd1) + struct.pack(">h", test_int)
        )

    def test_int_16(self):
        # Min
        test_int = 32768
        self.encoder.encode(test_int)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xcd) + struct.pack(">H", test_int)
        )

        # Max
        test_int = 65535
        self.encoder.encode(test_int)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xcd) + struct.pack(">H", test_int)
        )

    def test_uint_32(self):
        # Min
        test_int = -2147483648
        self.encoder.encode(test_int)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xd2) + struct.pack(">i", test_int)
        )

        # Max
        test_int = 2147483647
        self.encoder.encode(test_int)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xd2) + struct.pack(">i", test_int)
        )

    def test_int_32(self):
        # Min
        test_int = 2147483648
        self.encoder.encode(test_int)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xce) + struct.pack(">I", test_int)
        )

        # Max
        test_int = 4294967295
        self.encoder.encode(test_int)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xce) + struct.pack(">I", test_int)
        )

    def test_uint_64(self):
        # Min
        test_int = -9223372036854775808
        self.encoder.encode(test_int)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xd3) + struct.pack(">q", test_int)
        )

        # Max
        test_int = 9223372036854775807
        self.encoder.encode(test_int)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xd3) + struct.pack(">q", test_int)
        )

    def test_int_64(self):
        # Min
        test_int = 9223372036854775808
        self.encoder.encode(test_int)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xcf) + struct.pack(">Q", test_int)
        )

        # Max
        test_int = 18446744073709551615
        self.encoder.encode(test_int)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xcf) + struct.pack(">Q", test_int)
        )


class TestDecode:
    @classmethod
    def setup_class(cls):
        cls.encoder = IntEncoder()
        cls.decoder = IntDecoder()
    
    def compare(self, test_int: int):
        self.encoder.encode(test_int)
        payload = Payload(self.encoder.get_payload().strip())
        first_byte = struct.unpack(">B", payload.byte())[0]
        self.decoder.decode(first_byte, payload)
        assert self.decoder.get_elem() == test_int

    def test_fixint_positive(self):
        # Min
        test_int = 0
        self.compare(test_int)

        # Max
        test_int = 0x7f
        self.compare(test_int)

    def test_fixint_negative(self):
        # Min
        test_int = -32
        self.compare(test_int)

        # Max
        test_int = -1
        self.compare(test_int)

    def test_uint_8(self):
        # Min
        test_int = -128
        self.compare(test_int)

        # Max
        test_int = -33
        self.compare(test_int)

    def test_int_8(self):
        # Min
        test_int = 128
        self.compare(test_int)

        # Max
        test_int = 255
        self.compare(test_int)

    def test_uint_16(self):
        # Min
        test_int = -32768
        self.compare(test_int)

        # Max
        test_int = 32767
        self.compare(test_int)

    def test_int_16(self):
        # Min
        test_int = 32768
        self.compare(test_int)

        # Max
        test_int = 65535
        self.compare(test_int)

    def test_uint_32(self):
        # Min
        test_int = -2147483648
        self.compare(test_int)

        # Max
        test_int = 2147483647
        self.compare(test_int)

    def test_int_32(self):
        # Min
        test_int = 2147483648
        self.compare(test_int)

        # Max
        test_int = 4294967295
        self.compare(test_int)

    def test_uint_64(self):
        # Min
        test_int = -9223372036854775808
        self.compare(test_int)

        # Max
        test_int = 9223372036854775807
        self.compare(test_int)

    def test_int_64(self):
        # Min
        test_int = 9223372036854775808
        self.compare(test_int)

        # Max
        test_int = 18446744073709551615
        self.compare(test_int)
