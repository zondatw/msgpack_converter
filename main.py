from config.settings import setup_log
setup_log("msgpack")

import json
from typing import List
from datetime import datetime
from decimal import Decimal

from msgpack.codec import encoder, decoder
from msgpack.codec.ext import ExtStruct
from msgpack.codec.timestamp import TimestampStruct

def convert_bytes_to_hex_list(data: bytes) -> List:
    hex_list = []
    hex_data = data.hex()
    for i in range(0, len(hex_data), 2):
        hex_list.append(hex_data[i:i+2])
    return hex_list

def dict_example():
    original_data = {
        "str": "測試",
        "byte": b"test",
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
        "timestamp": TimestampStruct(datetime.strptime("2021/07/17 22:30:45.123456", "%Y/%m/%d %H:%M:%S.%f"))
    }

    encoded_data = encoder(original_data)

    print(f"Length: {len(encoded_data)}")
    print(encoded_data)
    print(" ".join(convert_bytes_to_hex_list(encoded_data)))

def file_example(file_path: str, encoded_file_path: str):
    original_data = {}
    with open(file_path, "r") as f:
        content = f.read()
        original_data = json.loads(content)

    encoded_data = encoder(original_data)

    print(f"Length: {len(encoded_data)}")
    print(encoded_data)
    print(" ".join(convert_bytes_to_hex_list(encoded_data)))

    with open(encoded_file_path, "wb") as f:
        f.write(encoded_data)

def decode_example():
    original_data = {
        "str": "1",
        "int": -33,
        "None": None,
        "bool": False,
        "array": [None, False, True, "測試", b"test"],
        "float": 1.1,
    }

    encoded_data = encoder(original_data)

    print(f"Length: {len(encoded_data)}")
    print(encoded_data)
    print(" ".join(convert_bytes_to_hex_list(encoded_data)))

    decoded_data = decoder(encoded_data)

    print("==== decode ====")
    print(decoded_data)


if __name__ == "__main__":
    dict_example()
    file_example("./example.json", "./example.msgpack")
    decode_example()