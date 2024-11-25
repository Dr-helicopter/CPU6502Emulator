from bytes import *

max_reg = 256 ** 2


class Register:
    def __init__(self, value):
        self._Rbyte : Byte
        self._Lbyte : Byte
        if type(value) is str:
            value = value.lower()
            if len(value) == 4:
                self._Rbyte = (Byte(value[2:]))
                self._Lbyte = (Byte(value[:2]))
                return
        elif type(value) is int:
            value %= max_reg
            self._Rbyte = (Byte(value))
            self._Lbyte = (Byte(value // Byte.max_val))
            return
        elif type(value) is tuple:
            if len(value) == 2:
                if isinstance(value[0], int) and isinstance(value[1], int):
                    self._Rbyte = Byte(value[1])
                    self._Lbyte = Byte(value[0])
        else: raise ValueError

    def __getitem__(self, item : int):
        if item >= 8: return self._Rbyte[item]
        elif 8 > item >= 0: return self._Lbyte[item]


    # arithmetic operators --- start ---
    def __add__(self, other):
        if not isinstance(other, Register): other = Register(other)
        r = int(self._Rbyte) + int(other._Rbyte)
        l = int(self._Lbyte) + int(other._Lbyte) + (1 if r>Byte.max_val else 0)
        return Register((l, r))
    def __radd__(self, other):
        if not isinstance(other, Register): other = Register(other)
        r = int(self._Rbyte) + int(other._Rbyte)
        l = int(self._Lbyte) + int(other._Lbyte) + 1 if r > Byte.max_val else 0
        return Register((l, r))
    # arithmetic operators --- end ---


    # casting --- start ---
    def __int__(self): return int(self._Lbyte) * Byte.max_val + int(self._Rbyte)

    def __str__(self) -> str:
        return str(self._Lbyte) + " " + str(self._Rbyte)
    # casting ---end ---