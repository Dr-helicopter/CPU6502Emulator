from registers import Register
from bytes import Byte

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


	def start(self):
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
