from datetime import datetime

from msgpack.codec import encoder
from msgpack.codec import decoder
from msgpack.codec.ext import ExtStruct
from msgpack.codec.timestamp import TimestampStruct

class TestEncoder:
    def test_encoder(self):
        original_data = {
            "str": "測試",
            "byte": b"test",
            "float": 1.1,
            "int": -1,
            "None": None,
            "bool": False,
            "array": [True, True],
            "dict": {
                "test": "test",
                "test2": 2
            }
        }
        result = encoder(original_data)
        assert result == b"\x88\xa3\x73\x74\x72\xa6\xe6\xb8\xac\xe8\xa9\xa6\xa4\x62\x79\x74\x65\xc4\x04\x74\x65\x73\x74\xa5\x66\x6c\x6f\x61\x74\xca\x3f\x8c\xcc\xcd\xa3\x69\x6e\x74\xff\xa4\x4e\x6f\x6e\x65\xc0\xa4\x62\x6f\x6f\x6c\xc2\xa5\x61\x72\x72\x61\x79\x92\xc3\xc3\xa4\x64\x69\x63\x74\x82\xa4\x74\x65\x73\x74\xa4\x74\x65\x73\x74\xa5\x74\x65\x73\x74\x32\x02"

    def test_encoder_with_ext(self):
        original_data = {
            "str": "測試",
            "byte": b"test",
            "float": 1.1,
            "int": -1,
            "None": None,
            "bool": False,
            "array": [True, True],
            "dict": {
                "test": "test",
                "test2": 2
            },
            "ext": ExtStruct(1, b"test"),
            "timestamp": TimestampStruct(datetime.strptime("2021/07/17 22:30:45.123456", "%Y/%m/%d %H:%M:%S.%f"))
        }
        result = encoder(original_data)
        assert result == b"\x8a\xa3\x73\x74\x72\xa6\xe6\xb8\xac\xe8\xa9\xa6\xa4\x62\x79\x74\x65\xc4\x04\x74\x65\x73\x74\xa5\x66\x6c\x6f\x61\x74\xca\x3f\x8c\xcc\xcd\xa3\x69\x6e\x74\xff\xa4\x4e\x6f\x6e\x65\xc0\xa4\x62\x6f\x6f\x6c\xc2\xa5\x61\x72\x72\x61\x79\x92\xc3\xc3\xa4\x64\x69\x63\x74\x82\xa4\x74\x65\x73\x74\xa4\x74\x65\x73\x74\xa5\x74\x65\x73\x74\x32\x02\xa3\x65\x78\x74\xd6\x01\x74\x65\x73\x74\xa9\x74\x69\x6d\x65\x73\x74\x61\x6d\x70\xd7\xff\x1d\x6f\x28\x00\x60\xf2\xe9\x95"


class TestDecoder:
    def test_decoder(self):
        original_data = {
            "str": "測試",
            "byte": b"test",
            "float": float("1.0"),
            "int": -1,
            "None": None,
            "bool": False,
            "array": [True, True],
            "dict": {
                "test": "test",
                "test2": 2
            }
        }
        encoded_data = encoder(original_data)
        decoded_data = decoder(encoded_data)
        assert decoded_data == original_data

    def test_decoder_with_ext(self):
        original_data = {
            "str": "測試",
            "byte": b"test",
            "float": float("1.0"),
            "int": -1,
            "None": None,
            "bool": False,
            "array": [True, True],
            "dict": {
                "test": "test",
                "test2": 2
            },
            "ext": ExtStruct(1, b"test"),
        }
        encoded_data = encoder(original_data)
        decoded_data = decoder(encoded_data)
        assert decoded_data == original_data