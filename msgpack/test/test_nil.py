import struct

from msgpack.core.base import Payload
from msgpack.codec.nil import Encoder as NilEncoder
from msgpack.codec.nil import Decoder as NilDecoder

class TestEncode:
    @classmethod
    def setup_class(cls):
        cls.encoder = NilEncoder()

    def test_result(self):
        self.encoder.encode(None)
        assert self.encoder.get_payload() == struct.pack("B", 0xc0)

class TestDecode:
    @classmethod
    def setup_class(cls):
        cls.decoder = NilDecoder()

    def test_result(self):
        first_byte = 0xc0
        payload = Payload()
        self.decoder.decode(first_byte, payload)
        assert self.decoder.get_elem() == None