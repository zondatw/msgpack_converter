import pytest

from msgpack.core.base import Payload
from msgpack.core.exceptions import PayloadOutOfRange

class TestPayload:
    def test_byte(self):
        test_byte = b"\xcc"
        payload = Payload(test_byte.strip())
        assert payload.byte() == test_byte

    def test_bytes(self):
        test_byte = b"\xcc\x11\x22\x33"
        payload = Payload(test_byte.strip())
        assert payload.bytes(len(test_byte)) == test_byte

    def test_get_all(self):
        test_byte = b"\xcc\x11\x22\x33\x44\x55\x66"
        payload = Payload(test_byte.strip())
        assert payload.get_all() == test_byte

    def test_is_empty(self):
        test_byte = b""
        payload = Payload(test_byte.strip())
        assert payload.is_empty() == True

    def test_out_of_range(self):
        test_byte = b""
        payload = Payload(test_byte.strip())

        with pytest.raises(PayloadOutOfRange):
            payload.byte()