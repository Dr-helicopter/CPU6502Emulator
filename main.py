from C6502 import CPU6519
from mem import Mem

cpu = CPU6519()
cpu.reset()
mem = Mem()
cpu.execute(mem, 2)

