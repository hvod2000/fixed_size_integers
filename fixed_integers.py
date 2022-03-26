import ctypes


class Int:
    def __init__(self, *args):
        if len(args) == 2:
            value, size = args
            self.bits = [ctypes.c_ubyte((value >> i) & 1) for i in range(size)]
        elif len(args) == 1:
            self.bits = args[0]
        else:
            raise Exception()
