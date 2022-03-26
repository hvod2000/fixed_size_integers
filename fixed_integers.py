import ctypes
from functools import reduce


class Int:
    def __init__(self, *args):
        if len(args) == 2:
            value, size = args
            self.bits = [ctypes.c_ubyte((value >> i) & 1) for i in range(size)]
        elif len(args) == 1:
            self.bits = args[0]
        else:
            raise Exception()

    def split(self, *sizes):
        assert len(self.bits) == sum(sizes)
        sizes = reduce(lambda lt, s: lt + [(s, sum(lt[-1]))], sizes, [(0, 0)])
        yield from (Int(self.bits[off : off + size]) for size, off in sizes)

    def __matmul__(self, other):
        return Int(self.bits + other.bits)

    def __imatmul__(self, value):
        self.value = value.u if isinstance(value, Int) else value
        return self

    def __str__(self):
        return f"{self.i}:i{len(self.bits)}"

    @property
    def value(self):
        return sum(b.value * 2**p for p, b in enumerate(self.bits))

    @value.setter
    def set_value(self, value):
        for i, bit in enumerate(self.bits):
            bit.value = (value >> i) & 1

    @property
    def u(self):
        return self.value

    @property
    def i(self):
        value, size = self.value, len(self.bits)
        return (value - 2 ** (size - 1)) % 2**size - 2 ** (size - 1)
