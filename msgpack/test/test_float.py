import pytest
import struct

from msgpack.codec.float import Encoder as float_encoder

class TestEncode:
    @classmethod
    def setup_class(cls):
        cls.encoder = float_encoder()

    def test_32(self):
        # Min
        test_float = 1.2E-38
        self.encoder.encode(test_float)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xca) + struct.pack(">f", test_float)
        )

        # Max
        test_float = 3.4E+38
        self.encoder.encode(test_float)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xca) + struct.pack(">f", test_float)
        )

    def test_64(self):
        # Min
        test_float = 2.3E-308
        self.encoder.encode(test_float)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xcb) + struct.pack(">d", test_float)
        )

        # Max
        test_float = 1.7E+308
        self.encoder.encode(test_float)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xcb) + struct.pack(">d", test_float)
        )

    def test_inf(self):
        # Min
        test_float = float("-inf")
        self.encoder.encode(test_float)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xcb) + struct.pack(">d", test_float)
        )

        # Max
        test_float = float("inf")
        self.encoder.encode(test_float)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xcb) + struct.pack(">d", test_float)
        )

    def test_nan(self):
        test_float = float("nan")
        self.encoder.encode(test_float)
        assert self.encoder.get_payload() == (
            struct.pack(">B", 0xcb) + struct.pack(">d", test_float)
        )
