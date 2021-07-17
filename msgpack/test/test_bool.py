import struct

from msgpack.codec.bool import Encoder as BoolEncoder

class TestEncode:
    @classmethod
    def setup_class(cls):
        cls.encoder = BoolEncoder()

    def test_true(self):
        self.encoder.encode(True)
        assert self.encoder.get_payload() == struct.pack("B", 0xc3)

    def test_false(self):
        self.encoder.encode(False)
        assert self.encoder.get_payload() == struct.pack("B", 0xc2)