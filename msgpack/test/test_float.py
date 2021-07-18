import math
import struct

import pytest

from msgpack.core.base import Payload
from msgpack.codec.float import Encoder as FloatEncoder
from msgpack.codec.float import Decoder as FloatDecoder

class TestEncode:
    @classmethod
    def setup_class(cls):
        cls.encoder = FloatEncoder()

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

class TestDecode:
    @classmethod
    def setup_class(cls):
        cls.encoder = FloatEncoder()
        cls.decoder = FloatDecoder()
    
    def compare(self, test_float: float):
        self.encoder.encode(test_float)
        payload = Payload(self.encoder.get_payload().strip())
        first_byte = struct.unpack(">B", payload.byte())[0]
        self.decoder.decode(first_byte, payload)
        assert math.isclose(self.decoder.get_elem(), test_float, rel_tol=1E-7)

    def test_32(self):
        # Min
        test_float = 1.2E-38
        self.compare(test_float)

        # Max
        test_float = 3.4E+38
        self.compare(test_float)

    def test_64(self):
        # Min
        test_float = 2.3E-308
        self.compare(test_float)

        # Max
        test_float = 1.7E+308
        self.compare(test_float)

    def test_inf(self):
        # Min
        test_float = float("-inf")
        self.compare(test_float)

        # Max
        test_float = float("inf")
        self.compare(test_float)

    def test_nan(self):
        test_float = float("nan")
        self.encoder.encode(test_float)
        payload = Payload(self.encoder.get_payload().strip())
        first_byte = struct.unpack(">B", payload.byte())[0]
        self.decoder.decode(first_byte, payload)
        assert math.isnan(self.decoder.get_elem())