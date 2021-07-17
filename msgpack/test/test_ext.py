import pytest
import struct


from msgpack.core.limitations import MIN_EXT_TYPE, MAX_EXT_TYPE, MIN_EXT_DATA_LEN, MAX_EXT_DATA_LEN
from msgpack.codec.ext import Encoder as ExtEncoder
from msgpack.codec.ext import ExtStruct
from msgpack.core.exceptions import ExtTypeOutOfRange, ExtDataOutOfRange


class TestStruct:
    def test_type_out_of_range(self):
        with pytest.raises(ExtTypeOutOfRange):
            ExtStruct(MIN_EXT_TYPE - 1, b"\x11")

        with pytest.raises(ExtTypeOutOfRange):
            ExtStruct(MAX_EXT_TYPE + 1, b"\x11")

    def test_data_out_of_range(self):
        with pytest.raises(ExtDataOutOfRange):
            ExtStruct(1, b"\x11" * (MIN_EXT_DATA_LEN - 1))

        with pytest.raises(ExtDataOutOfRange):
            ExtStruct(1, b"\x11" * (MAX_EXT_DATA_LEN + 1))


class TestEncode:
    @classmethod
    def setup_class(cls):
        cls.encoder = ExtEncoder()

    def test_fixext_1(self):
        test_ext = ExtStruct(1, b"\x11")
        self.encoder.encode(test_ext)
        length = len(test_ext.data)
        assert self.encoder.get_payload() == (
            struct.pack(">Bb", 0xd4, test_ext.type) + struct.pack(f"{length}s", test_ext.data)
        )

    def test_fixext_2(self):
        test_ext = ExtStruct(1, b"\x11\x22")
        self.encoder.encode(test_ext)
        length = len(test_ext.data)
        assert self.encoder.get_payload() == (
            struct.pack(">Bb", 0xd5, test_ext.type) + struct.pack(f"{length}s", test_ext.data)
        )

    def test_fixext_4(self):
        test_ext = ExtStruct(1, b"\x11\x22\x33\x44")
        self.encoder.encode(test_ext)
        length = len(test_ext.data)
        assert self.encoder.get_payload() == (
            struct.pack(">Bb", 0xd6, test_ext.type) + struct.pack(f"{length}s", test_ext.data)
        )

    def test_fixext_8(self):
        test_ext = ExtStruct(1, b"\x11\x22\x33\x44\x55\x66\x77\x88")
        self.encoder.encode(test_ext)
        length = len(test_ext.data)
        assert self.encoder.get_payload() == (
            struct.pack(">Bb", 0xd7, test_ext.type) + struct.pack(f"{length}s", test_ext.data)
        )

    def test_fixext_16(self):
        test_ext = ExtStruct(1, b"\x11\x22\x33\x44\x55\x66\x77\x88\x99\xaa\xbb\xcc\xdd\xee\xff\x00")
        self.encoder.encode(test_ext)
        length = len(test_ext.data)
        assert self.encoder.get_payload() == (
            struct.pack(">Bb", 0xd8, test_ext.type) + struct.pack(f"{length}s", test_ext.data)
        )

    def test_ext_8(self):
        # Min
        test_ext = ExtStruct(1, ("1" * 17).encode())
        self.encoder.encode(test_ext)
        length = len(test_ext.data)
        assert self.encoder.get_payload() == (
            struct.pack(">BBb", 0xc7, length, test_ext.type) + struct.pack(f"{length}s", test_ext.data)
        )

        # Max
        test_ext = ExtStruct(1, ("1" * ((2 ** 8) - 1)).encode())
        self.encoder.encode(test_ext)
        length = len(test_ext.data)
        assert self.encoder.get_payload() == (
            struct.pack(">BBb", 0xc7, length, test_ext.type) + struct.pack(f"{length}s", test_ext.data)
        )

    def test_ext_16(self):
        # Min
        test_ext = ExtStruct(1, ("1" * (2 ** 8)).encode())
        self.encoder.encode(test_ext)
        length = len(test_ext.data)
        assert self.encoder.get_payload() == (
            struct.pack(">BIb", 0xc8, length, test_ext.type) + struct.pack(f"{length}s", test_ext.data)
        )

        # Max
        test_ext = ExtStruct(1, ("1" * ((2 ** 16) - 1)).encode())
        self.encoder.encode(test_ext)
        length = len(test_ext.data)
        assert self.encoder.get_payload() == (
            struct.pack(">BIb", 0xc8, length, test_ext.type) + struct.pack(f"{length}s", test_ext.data)
        )

    def test_ext_32_min(self):
        # Min
        test_ext = ExtStruct(1, ("1" * (2 ** 16)).encode())
        self.encoder.encode(test_ext)
        length = len(test_ext.data)
        assert self.encoder.get_payload() == (
            struct.pack(">BLb", 0xc9, length, test_ext.type) + struct.pack(f"{length}s", test_ext.data)
        )

    @pytest.mark.slow
    def test_32_max(self):
        # Max
        test_ext = ExtStruct(1, ("1" * ((2 ** 32) - 1)).encode())
        self.encoder.encode(test_ext)
        length = len(test_ext.data)
        assert self.encoder.get_payload() == (
            struct.pack(">BLb", 0xc9, length, test_ext.type) + struct.pack(f"{length}s", test_ext.data)
        )
