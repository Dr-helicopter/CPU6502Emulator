from argparse import ArgumentTypeError




ByteTuple = tuple[int, int, int, int, int, int, int, int]

def _make_all_bytes(depth: int) -> list:
    if depth > 0:
        a = _make_all_bytes(depth - 1)
        b = []
        for i in a:
            b.append(i + (0,))
            b.append(i + (1,))
        return b
    return [()]

valid_bytes : frozenset[ByteTuple] = frozenset(ByteTuple(_make_all_bytes(8)))


def make_hex_from_tuple(t : ByteTuple):
    i : int = 1
    a : int = 0
    for b in t:
        a += b * i
        i *= 2
    r =  str(hex(a))[2:]
    return r if len(r) == 2 else '0' + r

def make_int_from_tuple(t : ByteTuple) -> int:
    i , n = 1 , 0
    for b in t:
        n += i * b
        i *= 2
    return n


_hex_to_tuple = {make_hex_from_tuple(i) : i for i in valid_bytes}
_tuple_to_hex = {_hex_to_tuple[a] : a for a in _hex_to_tuple}
_int_to_tuple = {make_int_from_tuple(i) : i for i in valid_bytes}
_tuple_to_int = {_int_to_tuple[a] : a for a in _int_to_tuple}
_int_to_hex = {i : _tuple_to_hex[_int_to_tuple[i]] for i in _int_to_tuple}
_hex_to_int = {_int_to_hex[i] : i for i in _int_to_hex}


class Byte:
    max_val = 0xff
    def __init__(self, value):
        self._value: int
        if type(value) is str:
            value = value.lower()
            if len(value) == 1: value = '0' + value
            if value in _hex_to_tuple:
                self._value = _hex_to_int[value]
        elif type(value) is int:
            value %= self.max_val+1
            self._value = value


    #assignment --- start ---
    def __iadd__(self, other): return self + other
    def __isub__(self, other): return self - other
    #assignment --- end ---

    # booleans ---start---
    def __eq__(self, other) -> bool:
        if not isinstance(other, bool): other = Byte(other)
        return self._value == other._value
    def __lt__(self, other) -> bool:
        if not isinstance(other, bool): other = Byte(other)
        return self._value < other._value
    def __gt__(self, other) -> bool:
        if not isinstance(other, bool): other = Byte(other)
        return self._value > other._value
    def __le__(self, other) -> bool:
        if not isinstance(other, bool): other = Byte(other)
        return self._value <= other._value
    def __ge__(self, other) -> bool:
        if not isinstance(other, bool): other = Byte(other)
        return self._value >= other._value
    # booleans ---end---

    # castings ---start---
    def __int__(self): return self._value
    def __str__(self) -> str:
        a = ''
        for i in _int_to_tuple[self._value]: a = str(i) + a
        return a
    def __hex__(self) -> str:
        return _int_to_hex[self._value]
    # casting ---end---




    # arithmetic operators --- start ---
    def __add__(self, other):
        if not isinstance(other, Byte): other = Byte(other)
        return Byte(self._value + other._value)
    def __radd__(self, other):
        if not isinstance(other, Byte): other = Byte(other)
        return Byte(self._value + other._value)
    def __sub__(self, other):
        if not isinstance(other, Byte): other = Byte(other)
        return Byte(self._value - other._value)
    def __rsub__(self, other):
        if not isinstance(other, Byte): other = Byte(other)
        return Byte(self._value - other._value)
    # arithmetic operators --- end ---

    def __getitem__(self, item) -> int:
        if type(item) != int: raise ArgumentTypeError("byte can only take int types")
        if not (0 <= item < 8): raise ValueError("byte can only take integers between 0 and 7")
        return _int_to_tuple[self._value][item]

