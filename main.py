from C6502 import CPU6519
from mem import Mem
import asm6502 as INS

cpu = CPU6519()
cpu.reset()
mem = Mem()
mem[0xfffc] = INS.LDA_ZP
mem[0xfffd] = 0x42
mem[0x42] = 0x23
cpu.execute(mem, 1)

print(hex(int(cpu.A)))