import logging

from .map import Encoder as MapEncoder
from .bin import Encoder as BinEncoder
from .str import Encoder as StrEncoder
from .int import Encoder as IntEncoder
from .float import Encoder as FloatEncoder
from .bool import Encoder as BoolEncoder
from .nil import Encoder as NilEncoder
from .array import Encoder as ArrayEncoder
from .ext import Encoder as ExtEncoder
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
            encoder = NilEncoder()
            encoder.encode(data)
        elif isinstance(data, bool):
            encoder = BoolEncoder()
            encoder.encode(data)
        elif isinstance(data, str):
            encoder = StrEncoder()
            encoder.encode(data)
        elif isinstance(data, bytes):
            encoder = BinEncoder()
            encoder.encode(data)
        elif isinstance(data, int):
            encoder = IntEncoder()
            encoder.encode(data)
        elif isinstance(data, float):
            encoder = FloatEncoder()
            encoder.encode(data)
        elif isinstance(data, ExtStruct):
            encoder = ExtEncoder()
            encoder.encode(data)
        elif isinstance(data, list):
            encoder = ArrayEncoder()
            encoder_gen = encoder.encode(data)
            for item in encoder_gen:
                logger.debug(f"Array: Check item: {item}")
                ret_payload = self._encode(item)
                logger.debug(f"Array: Check ret_payload: {ret_payload}")
                encoder_gen.send(ret_payload)
        elif isinstance(data, dict):
            encoder = MapEncoder()
            encoder_gen = encoder.encode(data)

            for key, value in encoder_gen:
                logger.debug(f"Dict: Check key: {key}, value: {value}")
                ret_payload = self._encode(key) + self._encode(value)
                logger.debug(f"Dict: Check ret_payload: {ret_payload}")
                encoder_gen.send(ret_payload)
        return encoder.get_payload()