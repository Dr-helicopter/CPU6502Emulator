from bytes import Byte
from registers import Register

class Mem:
    def __init__(self):
        self._data = {}

    max_mem = 1028 * 64

    def __getitem__(self, item) -> Byte:
        if not isinstance(item, (int, Byte, Register)): raise ValueError('noo')
        item = int(item)
        if item >= Mem.max_mem: raise IndexError('no')
        if not item in self._data: self._data[item] = Byte(0)
        return  self._data[item]

    def __setitem__(self, key, value : Byte) -> None:
        if not isinstance(key, (int, Byte, Register)): raise ValueError('noo')
        if key >= Mem.max_mem: raise IndexError('no')
        key = int(key)
        self._data[key] = value

