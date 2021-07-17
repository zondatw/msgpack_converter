from msgpack.codec import encoder
from msgpack.codec.ext import ExtStruct

class TestEncoder:
    def test_encoder(self):
        original_data = {
            "str": "1",
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
        assert result == b"\x87\xa3\x73\x74\x72\xa1\x31\xa5\x66\x6c\x6f\x61\x74\xca\x3f\x8c\xcc\xcd\xa3\x69\x6e\x74\xff\xa4\x4e\x6f\x6e\x65\xc0\xa4\x62\x6f\x6f\x6c\xc2\xa5\x61\x72\x72\x61\x79\x92\xc3\xc3\xa4\x64\x69\x63\x74\x82\xa4\x74\x65\x73\x74\xa4\x74\x65\x73\x74\xa5\x74\x65\x73\x74\x32\x02"

    def test_encoder_with_ext(self):
        original_data = {
            "str": "1",
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
        }
        result = encoder(original_data)
        assert result == b"\x88\xa3\x73\x74\x72\xa1\x31\xa5\x66\x6c\x6f\x61\x74\xca\x3f\x8c\xcc\xcd\xa3\x69\x6e\x74\xff\xa4\x4e\x6f\x6e\x65\xc0\xa4\x62\x6f\x6f\x6c\xc2\xa5\x61\x72\x72\x61\x79\x92\xc3\xc3\xa4\x64\x69\x63\x74\x82\xa4\x74\x65\x73\x74\xa4\x74\x65\x73\x74\xa5\x74\x65\x73\x74\x32\x02\xa3\x65\x78\x74\xd6\x01\x74\x65\x73\x74"
