import asm6502 as INS
from bytes import Byte, Cycle, Register


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


class CPU6519:
	def __init__(self):
		self.PC : Register = Register('fffc')
		self.SP : Register = Register('0100')

		self.A : Byte = Byte(0)
		self.X : Byte = Byte(0)
		self.Y : Byte = Byte(0)

		#flags VVV
		self.C : bool = False
		self.Z : bool = False
		self.I : bool = False
		self.D : bool = False
		self.B : bool = False
		self.V : bool = False
		self.N : bool = False


	def reset(self):
		self.PC = Register('fffc')
		self.SP = Register('0100')

		self.A = Byte(0)
		self.X = Byte(0)
		self.Y = Byte(0)

		self.C = False
		self.Z = False
		self.I = False
		self.D = False
		self.B = False
		self.V = False
		self.N = False



	def fetch_byte(self, mem : Mem, cycle : Cycle) -> Byte:
		data : Byte = mem[self.PC]
		self.PC += 1
		cycle.dec()
		return data

	def fetch_reg(self, mem : Mem, cycle : Cycle) -> Register:
		r : Byte = mem[self.PC]
		self.PC += 1
		cycle.dec()
		l : Byte = mem[self.PC]
		self.PC += 1
		cycle.dec()
		return Register((l, r))

	# set statuses --- start ---
	def lda_set_status(self):
		self.Z = self.A == 0
		self.N = self.A[7] == 1
	# set statuses --- end ---


	def execute(self, mem: Mem, cycle):
		if not isinstance(cycle, Cycle): cycle = Cycle(cycle)
		while cycle > 0:
			inst = self.fetch_byte(mem, cycle)

			match inst:

				case INS.JSR:
					sub_add = self.fetch_reg(mem, cycle)
					mem.write_word(self.SP, self.PC - 1, cycle)
					self.SP += 1
					cycle.dec()
					self.PC = sub_add
					cycle.dec()

				# LDA VVV
				case INS.LDA_IM: # immediate
					self.A = self.fetch_byte(mem, cycle)
					self.lda_set_status()
				case INS.LDA_ZP:
					zero_page_address = self.fetch_byte(mem, cycle)
					self.A = read_byte(mem, zero_page_address, cycle)
					self.lda_set_status()
				case INS.LDA_ZPX:
					zero_page_address = self.fetch_byte(mem, cycle)
					cycle.dec()
					self.A = read_byte(mem, Byte(zero_page_address + self.X), cycle)
					self.lda_set_status()

				case _: print('nothing to do')



def read_byte(mem : Mem, address : Byte, cycle : Cycle):
	data: Byte = mem[address]
	cycle.dec()
	return data
