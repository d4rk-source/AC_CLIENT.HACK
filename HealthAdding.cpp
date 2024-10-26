#include <iostream>
#include <Windows.h>
#include <tlhelp32.h>
#include <vector>

DWORD find_process(const std::wstring& name) {
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_PROCESS, 0);
    PROCESSENTRY32 processEntry;
    processEntry.dwSize = sizeof(PROCESSENTRY32);

    if (Process32First(snapshot, &processEntry)) {
        do {
            if (name == processEntry.szExeFile) {
                CloseHandle(snapshot);
                return processEntry.th32ProcessID;
            }
        } while (Process32Next(snapshot, &processEntry));
    }
    
    CloseHandle(snapshot);
    std::cout << "Process not found!" << std::endl;
    return 0;
}

uintptr_t get_module_base_address(DWORD processID, const std::wstring& moduleName) {
    uintptr_t baseAddress = 0;
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPMODULE | TH32CS_SNAPMODULE32, processID);
    MODULEENTRY32 moduleEntry;
    moduleEntry.dwSize = sizeof(MODULEENTRY32);

    if (Module32First(snapshot, &moduleEntry)) {
        do {
            if (moduleName == moduleEntry.szModule) {
                baseAddress = (uintptr_t)moduleEntry.modBaseAddr;
                break;
            }
        } while (Module32Next(snapshot, &moduleEntry));
    }
    
    CloseHandle(snapshot);
    return baseAddress;
}

uintptr_t get_pointer_value(HANDLE processHandle, uintptr_t baseAddress, const std::vector<uintptr_t>& offsets) {
    uintptr_t address = baseAddress;
    for (uintptr_t offset : offsets) {
        DWORD buffer;
        SIZE_T bytesRead;

        if (ReadProcessMemory(processHandle, (LPCVOID)address, &buffer, sizeof(buffer), &bytesRead)) {
            address = buffer + offset;
        } else {
            std::cout << "Failed to read memory at address: " << std::hex << address << std::endl;
            return 0;
        }
    }
    return address;
}

void write_memory(HANDLE processHandle, uintptr_t address, int value) {
    SIZE_T bytesWritten;
    WriteProcessMemory(processHandle, (LPVOID)address, &value, sizeof(value), &bytesWritten);
}

int main() {
    const std::wstring process_name = L"ac_client.exe";
    const std::wstring module_name = L"ac_client.exe";

    DWORD game_pid = find_process(process_name);
    if (game_pid == 0) return 1;

    HANDLE process_handle = OpenProcess(PROCESS_VM_READ | PROCESS_QUERY_INFORMATION | PROCESS_VM_WRITE, FALSE, game_pid);
    if (!process_handle) {
        std::cout << "Could not open process!" << std::endl;
        return 1;
    }

    uintptr_t base_address = get_module_base_address(game_pid, module_name);
    std::vector<uintptr_t> offsets = {0x0017E0A8, 0xEC};

    uintptr_t health_address = get_pointer_value(process_handle, base_address, offsets);
    std::cout << "Health address is: " << std::hex << health_address << std::endl;

    write_memory(process_handle, health_address, 9999);

    CloseHandle(process_handle);
    return 0;
}