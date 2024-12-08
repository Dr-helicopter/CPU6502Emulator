import asm6502 as INS
from bytes import Byte , Cycle
from registers import Register
from mem import Mem




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
