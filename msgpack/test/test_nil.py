import struct

from msgpack.codec.nil import Encoder as nil_encoder

class TestEncode:
    @classmethod
    def setup_class(cls):
        cls.encoder = nil_encoder()

    def test_result(self):
        self.encoder.encode(None)
        assert self.encoder.get_payload() == struct.pack("B", 0xc0)