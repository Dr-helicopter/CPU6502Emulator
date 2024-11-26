from bytes import Byte
from registers import Register
from mem import Mem

class Cycle:
	def __init__(self, value : int): self.value = value
	def inc(self): self.value += 1
	def dec(self): self.value -= 1
	def __eq__(self, other): return self.value == other
	def __lt__(self, other): return self.value < other
	def __gt__(self, other): return self.value > other
	def __le__(self, other): return self.value <= other
	def __ge__(self, other): return self.value >= other
	def __repr__(self): return str(self.value)

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



	def fetch_byte(self, mem: Mem, cycle : Cycle) -> Byte:
		data : Byte = mem[self.PC]
		self.PC += 1
		cycle.dec()
		return data




	def execute(self, mem: Mem, cycle):
		if not isinstance(cycle, Cycle): cycle = Cycle(cycle)
		while cycle > 0:
			inst = self.fetch_byte(mem, cycle)
			match inst:
				# LDA VVV
				case 0xA9: # immediate
					self.A = self.fetch_byte(mem, cycle)
					self.Z = self.A == 0
					self.N = self.A[7] == 1
				case _: print('nothing to do')










