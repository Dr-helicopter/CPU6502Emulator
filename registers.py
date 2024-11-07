from bytes import *

max_reg = 256 ** 2


class Register:
    def __init__(self, value):
        if type(value) is str:
            value = value.lower()
            if len(value) == 4:
                self._Rbyte = (Byte(value[2:]))
                self._Lbyte = (Byte(value[:2]))
        elif type(value) is int:
            value %= max_reg
            self._Rbyte = (Byte(value))
            self._Lbyte = (Byte(int(value / max_byte_val)))

    def __getitem__(self, item : int):
        if item >= 8: return self._Rbyte[item]
        elif 8 > item >= 0: return self._Lbyte[item]


    def __str__(self) -> str:
        return str(self._Lbyte) + " " + str(self._Rbyte)