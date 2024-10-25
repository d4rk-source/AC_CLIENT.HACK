from win32 import win32api
import psutil
import ctypes
from ctypes import wintypes

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


ammo_address = 0x00782E54

def write_memory(process_handle, address, value):
    """Write a value to the specified memory address of the process."""
    ctypes.windll.kernel32.WriteProcessMemory(process_handle, address, ctypes.byref(ctypes.c_int(value)), 4, None)

write_memory(process_handle, ammo_address, 9999)