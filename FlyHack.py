from pymem import *
from pymem.process import * #pymem is for reding memory
import keyboard
import time

shortcut = "space"
mem = Pymem("ac_client.exe") #attaches to the game
module = module_from_name(mem.process_handle, "ac_client.exe").lpBaseOfDll # gets the address of "ac_client.exe"
offsets = [0x30]

def getPointerAddr(base, offsets):
    addr = mem.read_int(base)
    for offset in offsets:
        if offset != offsets[-1]:
            addr = mem.read_int(addr + offset)
        addr = addr + offsets[-1]
    return addr


#cant figure this part out, allways gives error that it cant read at that address
# print(getPointerAddr(module + 0x00183828, offsets))

while True:
    if keyboard.is_pressed(shortcut):
        # mem.write_int(getPointerAddr(module + 0x0017E0A8, offsets), 1050000000)
        time.sleep(0.1)
        addme = mem.read_int(getPointerAddr(module + 0x0017E0A8, offsets))
        # print(addme)
        if str(addme)[0] == "-":
            while mem.read_int(getPointerAddr(module + 0x0017E0A8, offsets)) < 0:
                while keyboard.is_pressed(shortcut):
                    addme -= 25000     
                    mem.write_int(getPointerAddr(module + 0x0017E0A8, offsets), addme)
                    time.sleep(0.001)
                    if -1073995490 > mem.read_int(getPointerAddr(module + 0x0017E0A8, offsets)):
                        addme = 1045353216
                        mem.write_int(getPointerAddr(module + 0x0017E0A8, offsets), 0)
                        mem.write_int(getPointerAddr(module + 0x0017E0A8, offsets), addme)
                        while keyboard.is_pressed(shortcut):
                            addme += 25000
                            mem.write_int(getPointerAddr(module + 0x0017E0A8, offsets), addme)
                            time.sleep(0.001)
        else:
            while keyboard.is_pressed(shortcut):
                addme += 25000
                mem.write_int(getPointerAddr(module + 0x0017E0A8, offsets), addme)
                time.sleep(0.001)
