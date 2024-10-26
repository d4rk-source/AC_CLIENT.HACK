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

import ctypes
from ctypes import wintypes

def get_final_pointer_address(process_handle, base_address, offsets):
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
    
    # Set up ReadProcessMemory function
    kernel32.ReadProcessMemory.argtypes = [
        wintypes.HANDLE,         # hProcess
        wintypes.LPCVOID,        # lpBaseAddress
        wintypes.LPVOID,         # lpBuffer
        ctypes.c_size_t,         # nSize
        ctypes.POINTER(ctypes.c_size_t)  # lpNumberOfBytesRead
    ]
    kernel32.ReadProcessMemory.restype = wintypes.BOOL
    
    # Start from the base address
    address = base_address
    
    for offset in offsets:
        # Calculate the address with the current offset
        address = address + offset
        
        # Read the pointer at the current address
        buffer = ctypes.c_uint32()
        bytes_read = ctypes.c_size_t()
        
        if not kernel32.ReadProcessMemory(process_handle, address, ctypes.byref(buffer), ctypes.sizeof(buffer), ctypes.byref(bytes_read)):
            print("error krc")
        
        # Move to the next address in the chain
        address = buffer.value
    
    return address


process_name = "ac_client.exe"   # The process name you are targeting
module_name = "ac_client.exe"    # The module you're interested in

base_address = get_module_base_address(process_name, module_name)
offsets = [0x0017E0A8, 0xEC]
# cant get this thing to properly count it, the answer is wrong
health_address = get_final_pointer_address(process_name, base_address, offsets)
print(f"health address is: {health_address}")

def write_memory(process_handle, address, value):
    """Write a value to the specified memory address of the process."""
    ctypes.windll.kernel32.WriteProcessMemory(process_handle, address, ctypes.byref(ctypes.c_int(value)), 4, None)

write_memory(process_handle, health_address, 9999)

