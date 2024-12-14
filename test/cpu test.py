from C6502 import CPU6519, Mem
import unittest
import asm6502 as INS

cpu = CPU6519()
mem = Mem()


class Test_LDA(unittest.TestCase):
	def test_IM(self):
		cpu.reset()
		mem.reset()
		mem[0xfffc] = INS.LDA_IM
		mem[0xfffd] = 0x69
		cpu.execute(mem, 2)

		self.assertFalse(cpu.Z)
		self.assertFalse(cpu.N)
		self.unchanged_flags_test(cpu)
		self.assertEqual(cpu.A, 0x69)
		self.assertEqual(cpu.empty_cycles, 0)
		self.assertEqual(cpu.over_cycles, 0)

	def test_ZP(self):
		cpu.reset()
		mem.reset()
		mem[0xfffc] = INS.LDA_ZP
		mem[0xfffd] = 0x69
		mem[0x69] = 0x42
		cpu.execute(mem, 3)

		self.assertFalse(cpu.Z)
		self.assertFalse(cpu.N)
		self.unchanged_flags_test(cpu)
		self.assertEqual(cpu.A, 0x42)
		self.assertEqual(cpu.empty_cycles, 0)
		self.assertEqual(cpu.over_cycles, 0)

	def test_ZPX(self):
		cpu.reset()
		cpu.X = 0x5
		mem.reset()
		mem[0xfffc] = INS.LDA_ZPX
		mem[0xfffd] = 0x69
		mem[0x6e] = 0x42
		cpu.execute(mem, 4)

		self.assertFalse(cpu.Z)
		self.assertFalse(cpu.N)
		self.unchanged_flags_test(cpu)
		self.assertEqual(cpu.A, 0x42)
		self.assertEqual(cpu.empty_cycles, 0)
		self.assertEqual(cpu.over_cycles, 0)

	def test_ZPX_wrap(self):
		cpu.reset()
		cpu.X = 0xff
		mem.reset()
		mem[0xfffc] = INS.LDA_ZPX
		mem[0xfffd] = 0x80
		mem[0x7f] = 0x42
		cpu.execute(mem, 4)

		self.assertFalse(cpu.Z)
		self.assertFalse(cpu.N)
		self.unchanged_flags_test(cpu)
		self.assertEqual(cpu.A, 0x42)
		self.assertEqual(cpu.empty_cycles, 0)
		self.assertEqual(cpu.over_cycles, 0)

	def test_N_flag(self):
		cpu.reset()
		mem.reset()
		mem[0xfffc] = INS.LDA_IM
		mem[0xfffd] = 0xf0
		cpu.execute(mem, 2)

		self.assertFalse(cpu.Z)
		self.assertTrue(cpu.N)
		self.unchanged_flags_test(cpu)
		self.assertEqual(cpu.A, 0xf0)
		self.assertEqual(cpu.empty_cycles, 0)
		self.assertEqual(cpu.over_cycles, 0)

	def test_Z_flag(self):
		cpu.reset()
		mem.reset()
		mem[0xfffc] = INS.LDA_IM
		mem[0xfffd] = 0x0
		cpu.execute(mem, 2)

		self.assertTrue(cpu.Z)
		self.assertFalse(cpu.N)
		self.unchanged_flags_test(cpu)
		self.assertEqual(cpu.A, 0x0)
		self.assertEqual(cpu.empty_cycles, 0)
		self.assertEqual(cpu.over_cycles, 0)

		cpu.reset()
		mem.reset()
		mem[0xfffc] = INS.LDA_IM
		cpu.execute(mem, 2)

		self.assertTrue(cpu.Z)
		self.assertFalse(cpu.N)
		self.unchanged_flags_test(cpu)
		self.assertEqual(cpu.A, 0x0)
		self.assertEqual(cpu.empty_cycles, 0)
		self.assertEqual(cpu.over_cycles, 0)

	def unchanged_flags_test(self, c: CPU6519):
		self.assertFalse(cpu.C)
		self.assertFalse(cpu.I)
		self.assertFalse(cpu.D)
		self.assertFalse(cpu.B)
		self.assertFalse(cpu.V)


if __name__ == '__main__':
	unittest.main()
