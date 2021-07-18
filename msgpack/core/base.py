from msgpack.core.exceptions import PayloadOutOfRange

class Payload(list):
    def is_empty(self):
        return len(self) == 0

    def get_all(self):
        num = len(self)
        return self.bytes(num)

    def byte(self):
        return self.bytes(1)

    def bytes(self, num):
        if len(self) < num:
            raise PayloadOutOfRange(num, len(self))
        return bytes([self.pop(0) for _ in range(num)])