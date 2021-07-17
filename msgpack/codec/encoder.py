import logging

from .map import Encoder as map_encoder
from .bin import Encoder as bin_encoder
from .str import Encoder as str_encoder
from .int import Encoder as int_encoder
from .float import Encoder as float_encoder
from .bool import Encoder as bool_encoder
from .nil import Encoder as nil_encoder
from .array import Encoder as array_encoder
from .ext import Encoder as ext_encoder
from .ext import ExtStruct

logger = logging.getLogger(__name__)


class Encoder:
    def __init__(self):
        logger.info("Encoder")

    def encode(self, json_data):
        logger.info(f"Ready to encode: {json_data}")
        return self._encode(json_data)

    def _encode(self, data):
        logger.debug(f"Get data({type(data)}): {data}")
        encoder = None
        if data == None:
            encoder = nil_encoder()
            encoder.encode(data)
        elif isinstance(data, bool):
            encoder = bool_encoder()
            encoder.encode(data)
        elif isinstance(data, str):
            encoder = str_encoder()
            encoder.encode(data)
        elif isinstance(data, bytes):
            encoder = bin_encoder()
            encoder.encode(data)
        elif isinstance(data, int):
            encoder = int_encoder()
            encoder.encode(data)
        elif isinstance(data, float):
            encoder = float_encoder()
            encoder.encode(data)
        elif isinstance(data, ExtStruct):
            encoder = ext_encoder()
            encoder.encode(data)
        elif isinstance(data, list):
            encoder = array_encoder()
            encoder_gen = encoder.encode(data)
            for item in encoder_gen:
                logger.debug(f"Array: Check item: {item}")
                ret_payload = self._encode(item)
                logger.debug(f"Array: Check ret_payload: {ret_payload}")
                encoder_gen.send(ret_payload)
        elif isinstance(data, dict):
            encoder = map_encoder()
            encoder_gen = encoder.encode(data)

            for key, value in encoder_gen:
                logger.debug(f"Dict: Check key: {key}, value: {value}")
                ret_payload = self._encode(key) + self._encode(value)
                logger.debug(f"Dict: Check ret_payload: {ret_payload}")
                encoder_gen.send(ret_payload)
        return encoder.get_payload()