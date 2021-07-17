from config.settings import setup_log
setup_log("msgpack")

from typing import List

from msgpack.codec import encoder
from msgpack.codec.ext import ExtStruct

def convert_bytes_to_hex_list(data: bytes) -> List:
    hex_list = []
    hex_data = data.hex()
    for i in range(0, len(hex_data), 2):
        hex_list.append(hex_data[i:i+2])
    return hex_list


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

print(result)
print(" ".join(convert_bytes_to_hex_list(result)))