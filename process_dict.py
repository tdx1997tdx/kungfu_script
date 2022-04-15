import os

process_dict = {}


def add(hwnd, pid):
    if process_dict.get(hwnd):
        process_dict[hwnd].append(pid)
    else:
        process_dict[hwnd] = [pid]


def delete(hwnd):
    try:
        pid = process_dict[hwnd].pop()
        os.kill(pid, 9)
        if process_dict[hwnd] == []:
            process_dict.pop(hwnd)
    except Exception as e:
        print(e)
