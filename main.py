from C6502 import CPU6519
from mem import Mem
import asm6502 as INS

cpu = CPU6519()
cpu.reset()
mem = Mem()
mem[0xfffc] = INS.JSR
mem[0xfffd] = 0x42
mem[0xfffe] = 0x42
mem[0x4242] = INS.LDA_IM
mem[0x4243] = 0x02

cpu.execute(mem, 9)

print(hex(int(cpu.A)))