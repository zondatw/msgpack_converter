import pytest
import struct

from msgpack.core.limitations import MAX_BIN_OBJ_LEN
from msgpack.codec.bin import Encoder as BinEncoder
from msgpack.core.exceptions import BinOutOfRange

class TestEncode:
    @classmethod
    def setup_class(cls):
        cls.encoder = BinEncoder()

    def test_8(self):
        # Min
        test_bytes = "".encode()
        self.encoder.encode(test_bytes)
        length = len(test_bytes)
        assert self.encoder.get_payload() == (
            struct.pack(">BB", 0xc4, length) + struct.pack(f"{length}s", test_bytes)
        )

        # Max
        test_bytes = ("1" * ((2 ** 8) - 1)).encode()
        self.encoder.encode(test_bytes)
        length = len(test_bytes)
        assert self.encoder.get_payload() == (
            struct.pack(">BB", 0xc4, length) + struct.pack(f"{length}s", test_bytes)
        )

    def test_16(self):
        # Min
        test_bytes = ("1" * (2 ** 8)).encode()
        self.encoder.encode(test_bytes)
        length = len(test_bytes)
        assert self.encoder.get_payload() == (
            struct.pack(">BH", 0xc5, length) + struct.pack(f"{length}s", test_bytes)
        )

        # Max
        test_bytes = ("1" * ((2 ** 16) - 1)).encode()
        self.encoder.encode(test_bytes)
        length = len(test_bytes)
        assert self.encoder.get_payload() == (
            struct.pack(">BH", 0xc5, length) + struct.pack(f"{length}s", test_bytes)
        )

    def test_32_min(self):
        # Min
        test_bytes = ("1" * (2 ** 16)).encode()
        self.encoder.encode(test_bytes)
        length = len(test_bytes)
        assert self.encoder.get_payload() == (
            struct.pack(">BI", 0xc6, length) + struct.pack(f"{length}s", test_bytes)
        )

    @pytest.mark.slow
    def test_32_max(self):
        # Max
        test_bytes = ("1" * MAX_BIN_OBJ_LEN).encode()
        self.encoder.encode(test_bytes)
        length = len(test_bytes)
        assert self.encoder.get_payload() == (
            struct.pack(">BI", 0xc6, length) + struct.pack(f"{length}s", test_bytes)
        )

    @pytest.mark.slow
    def test_out_of_range(self):
        test_bytes = ("1" * (MAX_BIN_OBJ_LEN + 1)).encode()
        with pytest.raises(BinOutOfRange):
            self.encoder.encode(test_bytes)
