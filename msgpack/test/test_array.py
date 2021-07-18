import logging
import struct
from typing import List

import pytest

from msgpack.core.base import Payload
from msgpack.core.limitations import MAX_ARRAY_ELEM_NUM
from msgpack.codec.array import Encoder as ArrayEncoder
from msgpack.codec.array import Decoder as ArrayDecoder
from msgpack.core.exceptions import ArrayOutOfRange


class TestEncode:
    @classmethod
    def setup_class(cls):
        cls.encoder = ArrayEncoder()

    def test_fixarray(self):
        base = int("10010000", 2)

        # Min
        test_array = []
        length = len(test_array)
        encode_gen = self.encoder.encode(test_array)
        for data in encode_gen:
            encode_gen.send(data)
        assert self.encoder.get_payload() == (
            struct.pack("B", base + length) + b"".join(test_array)
        )

        # Max
        test_array = [b"test"] * 15
        length = len(test_array)
        encode_gen = self.encoder.encode(test_array)
        for data in encode_gen:
            encode_gen.send(data)
        assert self.encoder.get_payload() == (
            struct.pack("B", base + length) + b"".join(test_array)
        )

    def test_16(self):
        # Min
        test_array = [b"test"] * 16
        length = len(test_array)
        encode_gen = self.encoder.encode(test_array)
        for data in encode_gen:
            encode_gen.send(data)
        assert self.encoder.get_payload() == (
            struct.pack(">BH", 0xdc, length) + b"".join(test_array)
        )

        # Max
        test_array = [b"test"] * ((2 ** 16) - 1)
        length = len(test_array)
        encode_gen = self.encoder.encode(test_array)
        for data in encode_gen:
            encode_gen.send(data)
        assert self.encoder.get_payload() == (
            struct.pack(">BH", 0xdc, length) + b"".join(test_array)
        )

    def test_32_min(self):
        # Min
        test_array = [b"test"] * (2 ** 16)
        length = len(test_array)
        encode_gen = self.encoder.encode(test_array)
        for data in encode_gen:
            encode_gen.send(data)
        assert self.encoder.get_payload() == (
            struct.pack(">BI", 0xdd, length) + b"".join(test_array)
        )


    @pytest.mark.slow
    def test_32_max(self):
        # Max
        test_array = [b"test"] * MAX_ARRAY_ELEM_NUM
        length = len(test_array)
        encode_gen = self.encoder.encode(test_array)
        for data in encode_gen:
            encode_gen.send(data)
        assert self.encoder.get_payload() == (
            struct.pack(">BI", 0xdd, length) + b"".join(test_array)
        )

    @pytest.mark.slow
    def test_out_of_range(self):
        test_array = [b"test"] * (MAX_ARRAY_ELEM_NUM + 1)
        with pytest.raises(ArrayOutOfRange):
            self.encoder.encode(test_array)


class TestDecode:
    @classmethod
    def setup_class(cls):
        cls.encoder = ArrayEncoder()
        cls.decoder = ArrayDecoder()

    def compare(self, test_array: List):
        encode_gen = self.encoder.encode(test_array)
        for data in encode_gen:
            encode_gen.send(data)
        payload = Payload(self.encoder.get_payload().strip())
        first_byte = struct.unpack(">B", payload.byte())[0]
        decoder_gen = self.decoder.decode(first_byte, payload)
        # decode generator
        for _ in decoder_gen:
            decoder_gen.send(b"test")
        assert len(self.decoder.get_elem()) == len(test_array)
        assert self.decoder.get_elem() == test_array

    def test_fixarray_min(self):
        # Min
        test_array = []
        self.compare(test_array)

    def test_fixarray_max(self):
        # Max
        test_array = [b"test"] * 15
        self.compare(test_array)

    def test_16_min(self):
        # Min
        test_array = [b"test"] * 16
        self.compare(test_array)

    def test_16_max(self):
        # Max
        test_array = [b"test"] * ((2 ** 16) - 1)
        self.compare(test_array)

    def test_32_min(self):
        # Min
        test_array = [b"test"] * (2 ** 16)
        self.compare(test_array)

    @pytest.mark.slow
    def test_32_max(self):
        # Max
        test_array = [b"test"] * MAX_ARRAY_ELEM_NUM
        self.compare(test_array)