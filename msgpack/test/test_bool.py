import struct

from msgpack.core.base import Payload
from msgpack.codec.bool import Encoder as BoolEncoder
from msgpack.codec.bool import Decoder as BoolDecoder

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

class TestDecode:
    @classmethod
    def setup_class(cls):
        cls.decoder = BoolDecoder()

    def test_true(self):
        payload = Payload(b"\xc3".strip())
        first_byte = struct.unpack(">B", payload.byte())[0]
        self.decoder.decode(first_byte, payload)
        assert self.decoder.get_elem() == True

    def test_false(self):
        payload = Payload(b"\xc2".strip())
        first_byte = struct.unpack(">B", payload.byte())[0]
        self.decoder.decode(first_byte, payload)
        assert self.decoder.get_elem() == False