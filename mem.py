from bytes import Byte , Cycle
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

    def __setitem__(self, key, value) -> None:
        if not isinstance(key, (int, Byte, Register)): raise ValueError('noo')
        if not isinstance(value, Byte): value = Byte(value)
        key = int(key)
        if key >= Mem.max_mem: raise IndexError('no')
        self._data[key] = value

    def write_word(self, address, value, cycle : Cycle) -> None:
        if not isinstance(address, (int, Byte, Register)): raise ValueError('noo')
        if not isinstance(value, Register): value = Register(value)
        address = int(address)
        if address >= Mem.max_mem: raise IndexError('no')
        self._data[address] = value.get_l_byte()
        self._data[address+1] = value.get_r_byte()
        cycle -= 2