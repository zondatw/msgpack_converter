MIN_INT_OBJ_VALUE = -(2 ** 63)      # a value of an Integer object is limited from -(2^63) upto (2^64)-1
MAX_INT_OBJ_VALUE = (2 ** 64) - 1
MAX_BIN_OBJ_LEN = (2 ** 32) - 1     # maximum length of a Binary object is (2^32)-1
MAX_STR_OBJ_SIZE = (2 ** 32) - 1    # maximum byte size of a String object is (2^32)-1
MAX_ARRAY_ELEM_NUM = (2 ** 32) - 1  # maximum number of elements of an Array object is (2^32)-1
MAX_MAP_KV_NUM = (2 ** 32) - 1      # maximum number of key-value associations of a Map object is (2^32)-1

MIN_EXT_TYPE = -128
MAX_EXT_TYPE = 127
MIN_EXT_DATA_LEN = 1
MAX_EXT_DATA_LEN = (2 ** 32) - 1