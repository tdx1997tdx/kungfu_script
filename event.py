from tool.game_tool import *
import threading
from log import logger


# 检测角色是否需要吃药
class MonitorDrugEvent(threading.Thread):
    def __init__(self, hwnd, yuzhi, kuajiejian):
        threading.Thread.__init__(self)
        self.hwnd = hwnd
        self.exit_flag = 0
        self.yuzhi = yuzhi
        self.kuajiejian = kuajiejian
        self.game_tool = KungfuGameTool(self.hwnd)

    def exit_event(self):
        self.exit_flag = 1

    def run(self):
        logger.info('监控是否要吃药')
        while self.exit_flag == 0:
            now_point_baifenbi = self.game_tool.get_now_person_blood() / self.game_tool.get_person_max_blood()
            if now_point_baifenbi * 100 < self.yuzhi:
                logger.info("当前血量百分比:%s,低于警戒线" % (now_point_baifenbi * 100))
                self.game_tool.keyboard_tool.keyboard_press_once(keyboard_map[self.kuajiejian])
            time.sleep(0.5)


# 检测角色是否停止移动
class MonitorStopEvent(threading.Thread):
    def __init__(self, hwnd):
        threading.Thread.__init__(self)
        self.is_stop = False
        self.hwnd = hwnd
        self.exit_flag = 0
        self.now_point = None
        self.last_point = None
        self.game_tool = KungfuGameTool(self.hwnd)

    def exit_event(self):
        self.exit_flag = 1

    def is_stop_one_time(self):
        if not self.now_point or not self.last_point:
            return False
        return self.now_point[0] == self.last_point[0] and self.now_point[1] == self.last_point[1]

    def run(self):
        logger.info('监控"是否停止"启动')
        while self.exit_flag == 0:
            self.now_point = self.game_tool.get_now_person_point()
            self.is_stop = self.is_stop_one_time()
            self.last_point = self.now_point
            time.sleep(0.5)


class PutThingsEvent(threading.Thread):
    def __init__(self, hwnd, pkg=2, bengin=15, end=35, step=1500):
        threading.Thread.__init__(self)
        self.hwnd = hwnd
        self.exit_flag = 0
        self.keyboard_tool = KeyboardTool(self.hwnd)
        self.kungfu_tool = KungfuGameTool(self.hwnd)
        self.pkg = pkg
        self.bengin = bengin
        self.end = end
        self.step = step

    def exit_event(self):
        self.exit_flag = 1

    def run(self):
        last_time = time.time()
        while self.exit_flag == 0:
            now_time = time.time()
            if now_time - last_time > self.step and not self.kungfu_tool.is_fighting():
                self.kungfu_tool.put_things_to_repo(self.pkg, self.bengin, self.end)
                last_time = now_time
            time.sleep(5)


class KeyBoardEvent(threading.Thread):
    def __init__(self, hwnd, key, step):
        threading.Thread.__init__(self)
        self.hwnd = hwnd
        self.exit_flag = 0
        self.stop_flag = 0
        self.keyboard_tool = KeyboardTool(self.hwnd)
        self.key = key
        self.step = step

    def exit_event(self):
        self.exit_flag = 1

    def start_event(self):
        self.stop_flag = 0

    def stop_event(self):
        self.stop_flag = 1

    def run(self):
        while self.exit_flag == 0:
            while self.stop_flag == 1:
                time.sleep(0.1)
            self.keyboard_tool.keyboard_press_once(keyboard_map[self.key])
            time.sleep(self.step)
