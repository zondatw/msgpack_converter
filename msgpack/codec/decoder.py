import logging
import struct

from msgpack.core.base import Payload
import msgpack.codec.timestamp as ext_timestamp

from .nil import Decoder as NilDecoder
from .bool import Decoder as BoolDecoder
from .array import Decoder as ArrayDecoder
from .str import Decoder as StrDecoder
from .bin import Decoder as BinDecoder
from .map import Decoder as MapDecoder
from .float import Decoder as FloatDecoder
from .int import Decoder as IntDecoder
from .ext import Decoder as ExtDecoder

logger = logging.getLogger(__name__)

# Register extionsion decoder
ExtDecoder.register_ext(ext_timestamp.TYPE, ext_timestamp.decode_struct)

class Decoder:
    def __init__(self):
        logger.debug("Decoder")

    def decode(self, original_payload: bytes):
        logger.debug(f"Ready to decode: {original_payload}")
        payload = Payload(original_payload.strip())
        return self._decode(payload)

    def _decode(self, payload: Payload):
        if payload.is_empty():
            return

        first_byte = struct.unpack(">B", payload.byte())[0]
        logger.debug(f"Get first byte: {hex(first_byte)}")
        decoder = None

        if (
            (0x00 <= first_byte <= 0x7f) # positive fixint
            or (
                first_byte in [
                    0xcc, # uint 8
                    0xcd, # uint 16
                    0xce, # uint 32
                    0xcf, # uint 64
                    0xd0, # int 8
                    0xd1, # int 16
                    0xd2, # int 32
                    0xd3, # int 64
                ]
            )
            or (0xe0 <= first_byte <= 0xff) # positive fixint
        ):
            decoder = IntDecoder()
            decoder.decode(first_byte, payload)
        elif (
            (0x80 <= first_byte <= 0x8f) # fixmap
            or (
                first_byte in [
                    0xde, # map 16
                    0xdf, # map 32
                ]
            )
        ):
            decoder = MapDecoder()
            decoder_gen = decoder.decode(first_byte, payload)
            for index in decoder_gen:
                logger.debug(f"Dict: item index: {index}")
                ret_key = self._decode(payload)
                ret_elem = self._decode(payload)
                logger.debug(f"Dict: ret key: {ret_key}, ret elem: {ret_elem}")
                decoder_gen.send((ret_key, ret_elem))
        elif (
            (0x90 <= first_byte <= 0x9f) # fixarray
            or (
                first_byte in [
                    0xdc, # array 16
                    0xdd, # array 32
                ]
            )
        ):
            decoder = ArrayDecoder()
            decoder_gen = decoder.decode(first_byte, payload)
            for index in decoder_gen:
                logger.debug(f"Array: item index: {index}")
                ret_elem = self._decode(payload)
                logger.debug(f"Array: ret elem: {ret_elem}")
                decoder_gen.send(ret_elem)
        elif (
            (0xa0 <= first_byte <= 0xbf) # fixstr
            or (
                first_byte in [
                    0xd9, # str 8
                    0xda, # str 16
                    0xdb, # str 32
                ]
            )
        ):
            decoder = StrDecoder()
            decoder.decode(first_byte, payload)
        elif first_byte == 0xc0: # nil
            decoder = NilDecoder()
            decoder.decode(first_byte, payload)
        elif first_byte in [
            0xc2, # false
            0xc3, # true
        ]:
            decoder = BoolDecoder()
            decoder.decode(first_byte, payload)
        elif first_byte in [
            0xc4, # bin 8
            0xc5, # bin 16
            0xc6, # bin 32
        ]:
            decoder = BinDecoder()
            decoder.decode(first_byte, payload)
        elif first_byte in [
            0xc7, # ext 8
            0xc8, # ext 16
            0xc9, # ext 32
            0xd4, # fixext 1
            0xd5, # fixext 2
            0xd6, # fixext 4
            0xd7, # fixext 8
            0xd8, # fixext 16
        ]:
            decoder = ExtDecoder()
            decoder.decode(first_byte, payload)
        elif first_byte in [
            0xca, # float 8
            0xcb, # float 16
        ]:
            decoder = FloatDecoder()
            decoder.decode(first_byte, payload)
        return decoder.get_elem()

