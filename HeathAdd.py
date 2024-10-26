from pymem import *
from pymem.process import *
import keyboard

shortcut = "F1"
mem = Pymem("ac_client.exe")
module = module_from_name(mem.process_handle, "ac_client.exe").lpBaseOfDll
offsets = [0xEC]

def getPointerAddr(base, offsets):
    addr = mem.read_int(base)
    for offset in offsets:
        if offset != offsets[-1]:
            addr = mem.read_int(addr + offset)
        addr = addr + offsets[-1]
    return addr

print(module)

while True:
    if keyboard.is_pressed(shortcut):
        mem.write_int(getPointerAddr(module + 0x0017E0A8, offsets), 999)
