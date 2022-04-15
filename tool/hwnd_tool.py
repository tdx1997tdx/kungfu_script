import win32gui
import win32process
import win32api


def get_pt_id(hwnd):
    if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
        thread_id, process_id = win32process.GetWindowThreadProcessId(hwnd)
        return thread_id, process_id
    return None


def get_process_handle(hwnd):
    process_id = win32process.GetWindowThreadProcessId(hwnd)[1]
    process_handle = win32api.OpenProcess(0x1F0FFF, False, process_id)
    return process_handle
