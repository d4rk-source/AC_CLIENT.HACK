from pymem import *
from pymem.process import * #pymem is for reding memory
import keyboard

shortcut = "F1"
mem = Pymem("ac_client.exe") #attaches to the game
module = module_from_name(mem.process_handle, "ac_client.exe").lpBaseOfDll # gets the address of "ac_client.exe"
offsets = [0x8, 0x9DC, 0x30, 0x668]

def getPointerAddr(base, offsets):
    addr = mem.read_int(base)
    for offset in offsets:
        if offset != offsets[-1]:
            addr = mem.read_int(addr + offset)
        addr = addr + offsets[-1]
    return addr

print(getPointerAddr(module + 0x00183828, offsets))

# while True:
#     if keyboard.is_pressed(shortcut):
#         mem.write_int(getPointerAddr(module + 0x00183828, offsets), 1095485876)
