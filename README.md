# MessagePack converter

## Example

```python
from msgpack.codec import encoder
from msgpack.codec.ext import ExtStruct

original_data = {
    "str": "1",
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
}

encoded_data = encoder(original_data)

"""
binary: b'\x89\xa3str\xa11\xa4byte\xc4\x04test\xa5float\xca?\x8c\xcc\xcd\xa3int\xff\xa4None\xc0\xa4bool\xc2\xa5array\x92\xc3\xc3\xa4dict\x82\xa4test\xa4test\xa5test2\x02\xa3ext\xd6\x01test'
hex: 89 a3 73 74 72 a1 31 a4 62 79 74 65 c4 04 74 65 73 74 a5 66 6c 6f 61 74 ca 3f 8c cc cd a3 69 6e 74 ff a4 4e 6f 6e 65 c0 a4 62 6f 6f 6c c2 a5 61 72 72 61 79 92 c3 c3 a4 64 69 63 74 82 a4 74 65 73 74 a4 74 65 73 74 a5 74 65 73 74 32 02 a3 65 78 74 d6 01 74 65 73 74
"""
```

### ExtStruct

```python
# example: id = 1, data = b"test
# define
ExtStruct(1, b"test")
```

## Test

### Quick

`$ pytest .`  

### Slow

> include large element test

`$ pytest --runslow`  
