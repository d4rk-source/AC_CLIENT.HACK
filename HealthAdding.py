from win32 import win32api
import psutil
import ctypes
from ctypes import wintypes
import pymem

def find_process(name):
    for proc in psutil.process_iter(['pid', 'name']):
        if name in proc.info['name']:
            return proc.info['pid']
    print("proccess not found!")

game_pid = find_process("ac_client.exe")

PROCESS_ALL_ACCESS = 0x1F0FFF

process_handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, game_pid)
if not process_handle:
    print("Could not open process!")
    exit(1)

def get_module_base_address(process_name, module_name):
    # Open the process by name
    pm = pymem.Pymem(process_name)
    
    # List all modules loaded by the process
    module = pymem.process.module_from_name(pm.process_handle, module_name)
    
    if module:
        return module.lpBaseOfDll  # Get the base address of the module
    else:
        return None

# Example usage:
process_name = "ac_client.exe"   # The process name you are targeting
module_name = "ac_client.exe"    # The module you're interested in

base_address = get_module_base_address(process_name, module_name)

# cant get this thing to properly count it, the answer is wrong
health_address = hex(base_address + int(0x0017E0A8) + int(0xEC))
print(health_address)

def write_memory(process_handle, address, value):
    """Write a value to the specified memory address of the process."""
    ctypes.windll.kernel32.WriteProcessMemory(process_handle, address, ctypes.byref(ctypes.c_int(value)), 4, None)

write_memory(process_handle, health_address, 9999)

