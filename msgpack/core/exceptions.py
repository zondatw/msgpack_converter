from .limitations import (
    MAX_MAP_KV_NUM, MAX_STR_OBJ_SIZE, MAX_BIN_OBJ_LEN,
    MIN_INT_OBJ_VALUE, MAX_INT_OBJ_VALUE,
    MAX_ARRAY_ELEM_NUM,
    MIN_EXT_TYPE, MAX_EXT_TYPE, MIN_EXT_DATA_LEN, MAX_EXT_DATA_LEN,
)

class OutOfRange(Exception):
    pass


class ArrayOutOfRange(OutOfRange):
    def __init__(self, length):
        self.length = length

    def __str__(self):
        return f"Current array length {self.length} bigger than {MAX_ARRAY_ELEM_NUM}"


class MapOutOfRange(OutOfRange):
    def __init__(self, key_number):
        self.key_number = key_number

    def __str__(self):
        return f"Current key-value associations number {self.key_number} bigger than {MAX_MAP_KV_NUM}"


class StrOutOfRange(OutOfRange):
    def __init__(self, length):
        self.length = length

    def __str__(self):
        return f"Current string size {self.length} bigger than {MAX_STR_OBJ_SIZE}"


class BinOutOfRange(OutOfRange):
    def __init__(self, length):
        self.length = length

    def __str__(self):
        return f"Current bin length {self.length} bigger than {MAX_BIN_OBJ_LEN}"


class IntOutOfRange(OutOfRange):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Current {self.value} not in {MIN_INT_OBJ_VALUE} ~ {MAX_INT_OBJ_VALUE}"


class ExtTypeOutOfRange(OutOfRange):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Current extension type value {self.value} not in {MIN_EXT_TYPE} ~ {MAX_EXT_TYPE}"


class ExtDataOutOfRange(OutOfRange):
    def __init__(self, length):
        self.length = length

    def __str__(self):
        return f"Current extension length {self.length} not in {MIN_EXT_DATA_LEN} ~ {MAX_EXT_DATA_LEN}"
