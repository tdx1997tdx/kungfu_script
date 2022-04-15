from tool.basic_tool import *
from config import *
from tool.hwnd_tool import *
import ctypes
import requests
import time
import hashlib
import base64
import json


class BasicGameTool:
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.keyboard_tool = KeyboardTool(self.hwnd)
        self.mouse_tool = MouseTool(self.hwnd)
        self.image_tool = ImageTool(self.hwnd)
        self.mem_tool = MemTool(self.hwnd)

    # 根据格子编号获取行列
    def get_row_and_col(self, cell_number):
        col = cell_number % cell_length_num
        row = int(cell_number / cell_length_num)
        return row, col

    def change_package(self, pkg):
        self.mouse_tool.double_click(*pkgs[pkg])  # 换背包

    def open_or_close_package(self):
        self.keyboard_tool.keyboard_press_once(keyboard_map["b"])

    def open_or_close_task(self):
        self.keyboard_tool.keyboard_press_once(keyboard_map["q"])

    def input_text(self, text):
        for i in text:
            if i == " ":
                key_code = 32
            elif (97 <= ord(i) <= 122):
                key_code = ord(i) - 32
            elif (48 <= ord(i) <= 57):
                key_code = ord(i)
            else:
                key_code = 0
            self.keyboard_tool.keyboard_press_once(key_code)


class KungfuGameTool(BasicGameTool):
    def __init__(self, hwnd):
        super().__init__(hwnd)
        self.process_handle = get_process_handle(self.hwnd)
        self.kernel32 = ctypes.windll.LoadLibrary("C:\Windows\System32\kernel32.dll")

    def camera_up(self, step):
        self.keyboard_tool.keyboard_press_once(keyboard_map["end"])
        self.input_text("freecamera 1")
        self.keyboard_tool.keyboard_press_once(keyboard_map["enter"])
        time.sleep(0.3)
        self.keyboard_tool.keyboard_press_once(keyboard_map["end"])
        self.mouse_tool.right_mouse_click(712, 408)
        time.sleep(0.05)
        self.mouse_tool.wheel_up(step)

    def camera_up2(self, step):
        self.keyboard_tool.keyboard_press_once(keyboard_map["end"])
        self.input_text("freecamera 0")
        self.keyboard_tool.keyboard_press_once(keyboard_map["enter"])
        time.sleep(0.3)
        self.keyboard_tool.keyboard_press_once(keyboard_map["end"])
        self.mouse_tool.right_mouse_click(712, 408)
        time.sleep(0.05)
        self.mouse_tool.wheel_up(step)

    def camera_down(self):
        self.keyboard_tool.keyboard_press_once(keyboard_map["end"])
        self.input_text("freecamera 0")
        self.keyboard_tool.keyboard_press_once(keyboard_map["enter"])
        time.sleep(0.3)
        self.keyboard_tool.keyboard_press_once(keyboard_map["end"])
        self.mouse_tool.right_mouse_click(712, 408)
        time.sleep(0.05)
        self.mouse_tool.wheel_down(30)

    # 将仓库放在第一个背包第一格上
    def put_things_to_repo(self, pkg_num, from_cell_num, to_cell_num):
        # 打开背包
        self.open_or_close_package()
        # 打开仓库
        self.mouse_tool.left_mouse_click(*pkgs[0])
        self.mouse_tool.right_mouse_click(*cell_first)
        # 换背包
        self.mouse_tool.left_mouse_click(*pkgs[pkg_num])
        for i in range(from_cell_num, to_cell_num):
            row, col = self.get_row_and_col(i)
            time.sleep(0.5)
            self.mouse_tool.right_mouse_click(cell_first[0] + col * cell_width,
                                              cell_first[1] + row * cell_width)  # 放入仓库
        # 关闭仓库
        self.mouse_tool.left_mouse_click(close_repo[0], close_repo[1])
        # 关闭背包
        self.open_or_close_package()

    def is_fighting(self):
        is_ok, x, y = self.image_tool.find_img('./img/fight.bmp', x1=160, y1=0, x2=250, y2=110)
        return False if is_ok == -1 else True

    def is_zaiwa(self):
        is_ok, x, y = self.image_tool.find_img('./img/kuangshi.bmp|./img/shu.bmp|./img/yaocao.bmp', x1=431, y1=6,
                                               x2=591,
                                               y2=36)
        return False if is_ok == -1 else True

    def chuansong(self):
        is_ok, x, y = self.image_tool.find_str('传送石', './img/chuansongshi.txt', x1=156, y1=105,
                                               x2=843,
                                               y2=544, sim=0.5)
        return x + 15, y + 25

    def get_now_person_point(self):
        data = ctypes.c_long()
        self.kernel32.ReadProcessMemory(int(self.process_handle), 0x0063AE40, ctypes.byref(data), 4, None)
        data2 = ctypes.c_long()
        self.kernel32.ReadProcessMemory(int(self.process_handle), data.value + 0x3254, ctypes.byref(data2), 4, None)
        data3 = ctypes.c_long()
        self.kernel32.ReadProcessMemory(int(self.process_handle), data2.value + 0x1688, ctypes.byref(data3), 4, None)
        data4 = ctypes.c_long()
        self.kernel32.ReadProcessMemory(int(self.process_handle), data3.value + 0x1680, ctypes.byref(data4), 4, None)
        data5 = ctypes.c_long()
        self.kernel32.ReadProcessMemory(int(self.process_handle), data3.value + 0x1684, ctypes.byref(data5), 4, None)
        return data4.value, data5.value

    def get_now_person_blood(self):
        data = ctypes.c_long()
        self.kernel32.ReadProcessMemory(int(self.process_handle), 0x0638988, ctypes.byref(data), 4, None)
        data2 = ctypes.c_long()
        self.kernel32.ReadProcessMemory(int(self.process_handle), data.value + 0xC0, ctypes.byref(data2), 4, None)
        return data2.value

    def get_person_max_blood(self):
        data = ctypes.c_long()
        self.kernel32.ReadProcessMemory(int(self.process_handle), 0x0638988, ctypes.byref(data), 4, None)
        data2 = ctypes.c_long()
        self.kernel32.ReadProcessMemory(int(self.process_handle), data.value + 0xC4, ctypes.byref(data2), 4, None)
        return data2.value
