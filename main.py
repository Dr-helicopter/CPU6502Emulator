from C6502 import CPU6519
from mem import Mem
from bytes import Byte

cpu = CPU6519()
cpu.reset()
mem = Mem()
mem[0xfffc] = 0xA9
mem[0xfffd] = 0x42
cpu.execute(mem, 2)
print(cpu.A)