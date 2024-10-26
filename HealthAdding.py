from win32 import win32api
import psutil
import ctypes
from ctypes import wintypes, windll
import pymem

def find_process(name):
    for proc in psutil.process_iter(['pid', 'name']):
        if name in proc.info['name']:
            return proc.info['pid']
    print("proccess not found!")

game_pid = find_process("ac_client.exe")
print(game_pid)
PROCESS_VM_READ = 0x0010
PROCESS_QUERY_INFORMATION = 0x0400

process_handle = ctypes.windll.kernel32.OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION, False, game_pid)
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

import ctypes
from ctypes import wintypes

def get_pointer_value(process_handle, base_address, offsets):
    address = base_address
    for offset in offsets:
        buffer = ctypes.c_uint32()
        bytesRead = wintypes.DWORD()
        
        # Try reading memory and handle errors
        success = windll.kernel32.ReadProcessMemory(
            process_handle,
            ctypes.c_void_p(address),
            ctypes.byref(buffer),
            ctypes.sizeof(buffer),
            ctypes.byref(bytesRead)
        )
        
        if not success:
            error_code = windll.kernel32.GetLastError()
            raise Exception(f"Failed to read memory at address {hex(address)}. Error code: {error_code}")
        
        address = buffer.value + offset
    
    return address


process_name = "ac_client.exe"   # The process name you are targeting
module_name = "ac_client.exe"    # The module you're interested in

base_address = get_module_base_address(process_name, module_name)
offsets = [0x0017E0A8, 0xEC]
# cant get this thing to properly count it, the answer is wrong
health_address = get_pointer_value(process_name, base_address, offsets)
print(f"health address is: {health_address}")

def write_memory(process_handle, address, value):
    """Write a value to the specified memory address of the process."""
    ctypes.windll.kernel32.WriteProcessMemory(process_handle, address, ctypes.byref(ctypes.c_int(value)), 4, None)

write_memory(process_handle, health_address, 9999)

