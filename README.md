# MessagePack converter

## Quick start

`python main.py`  

## Example

### Python Dictionary

```python
from datetime import datetime

from msgpack.codec import encoder, decoder
from msgpack.codec.ext import ExtStruct
from msgpack.codec.timestamp import TimestampStruct

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

# Pass data to encoder function
encoded_data = encoder(original_data)

"""
Length: 113
b'\x8a\xa3str\xa6\xe6\xb8\xac\xe8\xa9\xa6\xa4byte\xc4\x04test\xa5float\xca?\x8c\xcc\xcd\xa3int\xff\xa4None\xc0\xa4bool\xc2\xa5array\x92\xc3\xc3\xa4dict\x82\xa4test\xa4test\xa5test2\x02\xa3ext\xd6\x01test\xa9timestamp\xd7\xff\x1do(\x00`\xf3Z\x15'
8a a3 73 74 72 a6 e6 b8 ac e8 a9 a6 a4 62 79 74 65 c4 04 74 65 73 74 a5 66 6c 6f 61 74 ca 3f 8c cc cd a3 69 6e 74 ff a4 4e 6f 6e 65 c0 a4 62 6f 6f 6c c2 a5 61 72 72 61 79 92 c3 c3 a4 64 69 63 74 82 a4 74 65 73 74 a4 74 65 73 74 a5 74 65 73 74 32 02 a3 65 78 74 d6 01 74 65 73 74 a9 74 69 6d 65 73 74 61 6d 70 d7 ff 1d 6f 28 00 60 f3 5a 15
"""

# Pass encoded data to decoder function
decoded_data = decoder(encoded_data)
""""
{'None': None,
 'array': [True, True],
 'bool': False,
 'byte': b'test',
 'dict': {'test': 'test', 'test2': 2},
 'ext': dGVzdA==,
 'float': 1.100000023841858,
 'int': -1,
 'str': '測試',
 'timestamp': 2021/07/17 22:30:45.123456+0000}
"""
```

#### ExtStruct

```python
# Example: type = 1, data = b"test
# Define
ExtStruct(1, b"test")

# 2021/07/17 22:30:45.123456+00:00
# Must be datetime
TimestampStruct(datetime.strptime("2021/07/17 22:30:45.123456+00:00", "%Y/%m/%d %H:%M:%S.%f%z"))
```

### File

> Note: File didn't support byte and extension types.

example.json  

```json
{
    "str": "測試",
    "float": 1.1,
    "int": -1,
    "None": null,
    "bool": false,
    "array": [true, true],
    "dict": {
        "test": "test",
        "test2": 2
    }
}
```

```python
import io
import json

from msgpack.codec import encoder, decoder

# Read json file and json unmarshal
original_data = {}
with io.open(file_path, "r", encoding="utf-8") as f:
    content = f.read()
    original_data = json.loads(content)

# Pass data to encoder function
encoded_data = encoder(original_data)

with open("./example.msgpack", "wb") as f:
    f.write(encoded_data)
"""
87 a3 73 74 72 a6 e6 b8 ac e8 a9 a6 a5 66 6c 6f 61 74 ca 3f 8c cc cd a3 69 6e 74 ff a4 4e 6f 6e 65 c0 a4 62 6f 6f 6c c2 a5 61 72 72 61 79 92 c3 c3 a4 64 69 63 74 82 a4 74 65 73 74 a4 74 65 73 74 a5 74 65 73 74 32 02
"""

# Read binary data
encoded_data = B""
with open("./example.msgpack", "rb") as f:
    encoded_data = f.read()

# Pass encoded data to decoder function
decoded_data = decoder(encoded_data)

# json marshal and store to file
with io.open("./example.msgpack.json", "w", encoding="utf-8") as f:
    json.dump(decoded_data, f, ensure_ascii=False)

"""
{'None': None,
 'array': [True, True],
 'bool': False,
 'dict': {'test': 'test', 'test2': 2},
 'float': 1.100000023841858,
 'int': -1,
 'str': '測試'}
"""
```

## Test

### Prerequisite

Install dependency, two ways:  

* pip: `pip install pytest pytest-cov`  
* poetry: `poetry install`  

### Quick test

`$ pytest .`  

coverage test:

`pytest --cov-config=.coveragerc --cov=. .`

### Slow test

> include large element test  
> Note: This test very slowly and possibly occurs `Memory Error`

`$ pytest --runslow`  

coverage test:

`pytest --cov-config=.coveragerc --cov=. --runslow`
