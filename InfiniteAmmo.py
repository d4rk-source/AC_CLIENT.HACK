from pymem import *
from pymem.process import * #pymem is for reding memory
import keyboard

mem = Pymem("ac_client.exe") #attaches to the game
module = module_from_name(mem.process_handle, "ac_client.exe").lpBaseOfDll # gets the address of "ac_client.exe"
offsets = [0x140]

def getPointerAddr(base, offsets):
    addr = mem.read_int(base)
    for offset in offsets:
        if offset != offsets[-1]:
            addr = mem.read_int(addr + offset)
        addr = addr + offsets[-1]
    return addr

while True:
    mem.write_int(getPointerAddr(module + 0x00195404, offsets), 69)
