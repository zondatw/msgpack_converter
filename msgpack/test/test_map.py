import struct
from typing import Dict

import pytest

from msgpack.core.base import Payload
from msgpack.core.limitations import MAX_MAP_KV_NUM
from msgpack.codec.map import Encoder as MapEncoder
from msgpack.codec.map import Decoder as MapDecoder
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


class TestDecode:
    @classmethod
    def setup_class(cls):
        cls.encoder = MapEncoder()
        cls.decoder = MapDecoder()
    
    def compare(self, test_map: Dict):
        encode_gen = self.encoder.encode(test_map)
        for key, value in encode_gen:
            encode_gen.send(key.encode() + value.encode())
        payload = Payload(self.encoder.get_payload().strip())
        first_byte = struct.unpack(">B", payload.byte())[0]
        decoder_gen = self.decoder.decode(first_byte, payload)
        # decode generator
        for index, _ in enumerate(decoder_gen):
            decoder_gen.send((str(index), str(index)))
        assert self.decoder.get_elem() == test_map

    def test_fixmap_min(self):
        # Min
        test_map = {}
        self.compare(test_map)

    def test_fixmap_max(self):
        # Max
        test_map = {}
        for i in range(15):
            test_map[str(i)] = str(i)
        self.compare(test_map)

    def test_16_min(self):
        # Min
        test_map = {}
        for i in range(16):
            test_map[str(i)] = str(i)
        self.compare(test_map)

    def test_16_max(self):
        # Max
        test_map = {}
        for i in range(((2 ** 16) - 1)):
            test_map[str(i)] = str(i)
        self.compare(test_map)

    def test_32_min(self):
        # Min
        test_map = {}
        for i in range(2 ** 16):
            test_map[str(i)] = str(i)
        self.compare(test_map)

    @pytest.mark.slow
    def test_32_max(self):
        # Max
        test_map = {}
        for i in range(MAX_MAP_KV_NUM):
            test_map[str(i)] = str(i)
        self.compare(test_map)