from typing import Final




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
    return str(hex(a))[2:]

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



class Byte:
    max_val = 256
    def __init__(self, value):
        if type(value) is str:
            value = value.lower()
            if len(value) == 1: value += '0'
            if value in _hex_to_tuple:
                self._value : Final[ByteTuple] = (_hex_to_tuple[value])
        elif type(value) is int:
            value %= self.max_val
            self._value = _hex_to_tuple[str(hex(value))[2:]]

    # basics
    def __getitem__(self, item) -> int:
        return self._value[-item + 1]
    def __str__(self) -> str:
        a = ''
        for i in self._value: a = str(i) + a
        return a
    def __hex__(self) -> str:
        return _tuple_to_hex[self._value]