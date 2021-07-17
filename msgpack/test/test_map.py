import pytest
import struct

from msgpack.core.limitations import MAX_MAP_KV_NUM
from msgpack.codec.map import Encoder as MapEncoder
from msgpack.core.exceptions import MapOutOfRange


class TestEncode:
    @classmethod
    def setup_class(cls):
        cls.encoder = MapEncoder()

    def test_fixmap(self):
        base = int("10000000", 2)

        # Min
        test_map = {}
        length = len(test_map)
        encode_gen = self.encoder.encode(test_map)
        for key, value in encode_gen:
            encode_gen.send(key.encode() + value.encode())

        checking_data = b""
        for key, value in test_map.items():
            checking_data += key.encode() + value.encode()

        assert self.encoder.get_payload() == (
            struct.pack("B", base + length) + checking_data
        )

        # Max
        test_map = {}
        for i in range(15):
            test_map[str(i)] = str(i)
        length = len(test_map)
        encode_gen = self.encoder.encode(test_map)
        for key, value in encode_gen:
            encode_gen.send(key.encode() + value.encode())

        checking_data = b""
        for key, value in test_map.items():
            checking_data += key.encode() + value.encode()

        assert self.encoder.get_payload() == (
            struct.pack("B", base + length) + checking_data
        )

    def test_16(self):
        # Min
        test_map = {}
        for i in range(16):
            test_map[str(i)] = str(i)
        length = len(test_map)
        encode_gen = self.encoder.encode(test_map)
        for key, value in encode_gen:
            encode_gen.send(key.encode() + value.encode())

        checking_data = b""
        for key, value in test_map.items():
            checking_data += key.encode() + value.encode()

        assert self.encoder.get_payload() == (
            struct.pack(">BH", 0xde, length) + checking_data
        )

        # Max
        test_map = {}
        for i in range(((2 ** 16) - 1)):
            test_map[str(i)] = str(i)
        length = len(test_map)
        encode_gen = self.encoder.encode(test_map)
        for key, value in encode_gen:
            encode_gen.send(key.encode() + value.encode())

        checking_data = b""
        for key, value in test_map.items():
            checking_data += key.encode() + value.encode()

        assert self.encoder.get_payload() == (
            struct.pack(">BH", 0xde, length) + checking_data
        )

    def test_32_min(self):
        # Min
        test_map = {}
        for i in range(2 ** 16):
            test_map[str(i)] = str(i)
        length = len(test_map)
        encode_gen = self.encoder.encode(test_map)
        for key, value in encode_gen:
            encode_gen.send(key.encode() + value.encode())

        checking_data = b""
        for key, value in test_map.items():
            checking_data += key.encode() + value.encode()

        assert self.encoder.get_payload() == (
            struct.pack(">BI", 0xdf, length) + checking_data
        )

    @pytest.mark.slow
    def test_32_max(self):
        # Max
        test_map = {}
        for i in range(MAX_MAP_KV_NUM):
            test_map[str(i)] = str(i)
        length = len(test_map)
        encode_gen = self.encoder.encode(test_map)
        for key, value in encode_gen:
            encode_gen.send(key.encode() + value.encode())

        checking_data = b""
        for key, value in test_map.items():
            checking_data += key.encode() + value.encode()

        assert self.encoder.get_payload() == (
            struct.pack(">BI", 0xdf, length) + checking_data
        )

    @pytest.mark.slow
    def test_out_of_range(self):
        test_map = {}
        for i in range(MAX_MAP_KV_NUM + 1):
            test_map[str(i)] = str(i)
        with pytest.raises(MapOutOfRange):
            self.encoder.encode(test_map)