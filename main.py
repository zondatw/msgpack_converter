from config.settings import setup_log
setup_log("msgpack", Debug=False)

import io
import json
from typing import List
from datetime import datetime
from pprint import pprint

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
    print(" Dict Example ".center(40, "*"))
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
        "timestamp": TimestampStruct(datetime.strptime("2021/07/17 22:30:45.123456+00:00", "%Y/%m/%d %H:%M:%S.%f%z")),
    }

    print(" Original json ".center(20, "="))
    pprint(original_data)

    print(" encode ".center(20, "="))
    encoded_data = encoder(original_data)
    print(f"Length: {len(encoded_data)}")
    print(encoded_data)
    print(" ".join(convert_bytes_to_hex_list(encoded_data)))

    print(" decode ".center(20, "="))
    decoded_data = decoder(encoded_data)
    pprint(decoded_data)

def file_example(file_path: str, encoded_file_path: str):
    print(" File Example ".center(40, "*"))
    original_data = {}
    with io.open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        original_data = json.loads(content)

    print(" Original json ".center(20, "="))
    pprint(original_data)

    print(" encode ".center(20, "="))
    encoded_data = encoder(original_data)
    with open(encoded_file_path, "wb") as f:
        f.write(encoded_data)

    encoded_data = B""
    with open(encoded_file_path, "rb") as f:
        encoded_data = f.read()
    print(f"Length: {len(encoded_data)}")
    print(encoded_data)
    print(" ".join(convert_bytes_to_hex_list(encoded_data)))

    print(" decode ".center(20, "="))
    decoded_data = decoder(encoded_data)
    pprint(decoded_data)

    with io.open(f"{encoded_file_path}.json", "w", encoding="utf-8") as f:
        json.dump(decoded_data, f, ensure_ascii=False)


if __name__ == "__main__":
    dict_example()
    print()
    file_example("./example.json", "./example.msgpack")