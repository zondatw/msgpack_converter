import struct

import pytest

from msgpack.core.limitations import MAX_STR_OBJ_SIZE
from msgpack.codec.str import Encoder as StrEncoder
from msgpack.core.exceptions import StrOutOfRange

class TestEncode:
    @classmethod
    def setup_class(cls):
        cls.encoder = StrEncoder()

    def test_fixstr(self):
        base = int("10100000", 2)

        # Min
        test_str = ""
        self.encoder.encode(test_str)
        test_encoded_str = test_str.encode("utf-8")
        length = len(test_encoded_str)
        assert self.encoder.get_payload() == (
            struct.pack("B", base + len(test_encoded_str)) + struct.pack(f"{length}s", test_encoded_str)
        )

        # Max
        test_str = "1" * 31
        self.encoder.encode(test_str)
        test_encoded_str = test_str.encode("utf-8")
        length = len(test_encoded_str)
        assert self.encoder.get_payload() == (
            struct.pack("B", base + len(test_encoded_str)) + struct.pack(f"{length}s", test_encoded_str)
        )

    def test_8(self):
        # Min
        test_str = "1" * 32
        self.encoder.encode(test_str)
        test_encoded_str = test_str.encode("utf-8")
        length = len(test_encoded_str)
        assert self.encoder.get_payload() == (
            struct.pack(">BB", 0xd9, length) + struct.pack(f"{length}s", test_encoded_str)
        )

        # Max
        test_str = "1" * ((2 ** 8) - 1)
        self.encoder.encode(test_str)
        test_encoded_str = test_str.encode("utf-8")
        length = len(test_encoded_str)
        assert self.encoder.get_payload() == (
            struct.pack(">BB", 0xd9, length) + struct.pack(f"{length}s", test_encoded_str)
        )

    def test_16(self):
        # Min
        test_str = "1" * (2 ** 8)
        self.encoder.encode(test_str)
        test_encoded_str = test_str.encode("utf-8")
        length = len(test_encoded_str)
        assert self.encoder.get_payload() == (
            struct.pack(">BH", 0xda, length) + struct.pack(f"{length}s", test_encoded_str)
        )

        # Max
        test_str = "1" * ((2 ** 16) - 1)
        self.encoder.encode(test_str)
        test_encoded_str = test_str.encode("utf-8")
        length = len(test_encoded_str)
        assert self.encoder.get_payload() == (
            struct.pack(">BH", 0xda, length) + struct.pack(f"{length}s", test_encoded_str)
        )

    def test_32_min(self):
        # Min
        test_str = "1" * (2 ** 16)
        self.encoder.encode(test_str)
        test_encoded_str = test_str.encode("utf-8")
        length = len(test_encoded_str)
        assert self.encoder.get_payload() == (
            struct.pack(">BI", 0xdb, length) + struct.pack(f"{length}s", test_encoded_str)
        )

    @pytest.mark.slow
    def test_32_max(self):
        # Max
        test_str = "1" * MAX_STR_OBJ_SIZE
        self.encoder.encode(test_str)
        test_encoded_str = test_str.encode("utf-8")
        length = len(test_encoded_str)
        assert self.encoder.get_payload() == (
            struct.pack(">BI", 0xdb, length) + struct.pack(f"{length}s", test_encoded_str)
        )

    @pytest.mark.slow
    def test_out_of_range(self):
        test_str = "1" * (MAX_STR_OBJ_SIZE + 1)
        with pytest.raises(StrOutOfRange):
            self.encoder.encode(test_str)
