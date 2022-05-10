from tool.basic_tool import *
from config import *
from game_config import *
from tool.hwnd_tool import *
import ctypes
import time
from log import logger


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

    def is_caishen(self):
        is_ok, x, y = self.image_tool.find_img('./img/caishen.bmp', x1=890, y1=180, x2=1020, y2=640)
        return False if is_ok == -1 else True

    def is_sudu(self):
        is_ok, x, y = self.image_tool.find_img('./img/sudu.bmp', x1=890, y1=180, x2=1020, y2=640)
        return False if is_ok == -1 else True

    def chuansong(self):
        is_ok, x, y = self.image_tool.find_str('传送石', './img/chuansongshi.txt', x1=156, y1=105,
                                               x2=843,
                                               y2=544, sim=0.5)
        return x + 15, y + 25

    def is_stop(self):
        x1, y1, x2, y2 = 948, 156, 1017, 169
        is_ok = self.image_tool.is_change_for_certain_place(x1, y1, x2, y2)
        return False if is_ok == 0 else True

    def is_eat_drug(self):
        col = self.image_tool.get_color(79, 68)
        if col[0] != "8" or col[2] != "0" or col[4] != "2":
            return True
        return False

    # 找到周莲香
    def find_npc_zhou(self):
        def find_zhoulianxiang():
            # is_ok, x, y = self.image_tool.find_img('./img/zhoulianxiang.bmp', x1=150, y1=90, x2=1000, y2=630, sim=0.5)
            is_ok, x, y = self.image_tool.find_str('周莲香', './img/zhoulianxiang.txt', x1=150, y1=90, x2=1000, y2=630,
                                                   sim=0.6)
            return x + 20, y + 20

        def find_qingbao():
            is_ok, x, y = self.image_tool.find_img('./img/qingbao.bmp', x1=150, y1=90, x2=1000, y2=630, sim=0.5)
            return False if is_ok == -1 else True

        time.sleep(1)
        x, y = find_zhoulianxiang()
        if x == -1 and y == -1:
            logger.info("没找到周莲香,继续递归查找")
            self.find_npc_zhou()
            return
        zhou_rel_x, zhou_rel_y = x, y
        self.mouse_tool.left_mouse_click(zhou_rel_x, zhou_rel_y)
        time.sleep(0.2)
        if not find_qingbao():
            logger.info("没找到情报,递归查找")
            self.find_npc_zhou()

    # 点击接取考古任务
    def get_task(self):
        self.mouse_tool.left_mouse_click(470, 450)
        time.sleep(0.2)
        self.mouse_tool.left_mouse_click(510, 410)

    # 打开任务栏，并且弄到最底下
    def open_task_set(self):
        self.open_or_close_task()
        time.sleep(0.1)
        self.mouse_tool.left_mouse_keep_press(1000, 385)
        time.sleep(0.5)
        self.mouse_tool.left_mouse_realse()
        self.mouse_tool.left_mouse_click(830, 388)

    # 判断是否是相关类型的任务
    def is_certain_task(self):
        is_ok, x, y = self.image_tool.find_img(kaogu_type_map[kaogu_config["type"]], x1=721, y1=429, x2=988, y2=514)
        return False if is_ok == -1 else True

    # 放弃任务
    def give_up_task(self):
        self.mouse_tool.left_mouse_click(860, 625)
        time.sleep(0.5)
        self.mouse_tool.left_mouse_click(450, 430)
        time.sleep(0.5)
        self.open_or_close_task()

    # 使用土地符后需要自动跑到考古坐标
    def location(self):
        # 定位
        self.mouse_tool.left_mouse_click(860, 440)
        time.sleep(0.3)
        self.mouse_tool.left_mouse_click(463, 428)
        time.sleep(0.3)
        self.open_or_close_task()

    # 找到宝藏
    def find_baozang(self):
        is_ok, x, y = self.image_tool.find_img('./img/getbaozang.bmp', x1=230, y1=300, x2=700, y2=490, sim=0.6)
        return False if is_ok == -1 else True

    # 是否被挡住
    def is_block(self):
        is_ok, x, y = self.image_tool.find_img('./img/block.bmp', x1=250, y1=10, x2=850, y2=200, sim=0.6)
        return False if is_ok == -1 else True

    # 是否在加载中
    def is_loading(self):
        is_ok, x, y = self.image_tool.find_img('./img/pkg.bmp', x1=780, y1=720, x2=1010, y2=770, sim=0.6)
        return True if is_ok == -1 else False
