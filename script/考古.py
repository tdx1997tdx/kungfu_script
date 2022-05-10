from event import *
import pythoncom
from game_config import kaogu_config
import random


class WaBao():
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.exit_flag = 0
        self.game_tool = KungfuGameTool(self.hwnd)
        self.keyboard_tool = KeyboardTool(self.hwnd)
        self.monitorStopEvent = MonitorStopEvent(self.hwnd)
        self.monitorDrugEvent = MonitorDrugEvent(self.hwnd, kaogu_config["drug"])
        self.start_thread()

    def start_thread(self):
        self.monitorStopEvent.start()
        self.monitorDrugEvent.start()

    def go_to_certain_place(self):
        time.sleep(1)
        self.keyboard_tool.keyboard_press_once(keyboard_map[kaogu_config["landmark"]])
        logger.info('使用地标')
        time.sleep(1)
        self.keyboard_tool.keyboard_press_once(keyboard_map[kaogu_config["jiezhi"]])
        logger.info('使用结婚戒指')

    def xunlu(self):
        self.game_tool.camera_down()
        cnt = 0
        while not self.game_tool.find_baozang():
            if self.monitorStopEvent.is_stop:
                cnt += 1
            else:
                cnt = 0
            logger.info('自动寻路中。。。。。,当前停止参数%s' % (cnt))
            if cnt > 20:
                logger.info("卡了,放弃原来任务重来")
                self.game_tool.open_or_close_task()
                self.game_tool.give_up_task()
                break
            time.sleep(0.5)
        logger.info('寻路函数结束')
        time.sleep(0.5)
        # 点击确定按钮
        self.game_tool.mouse_tool.left_mouse_click(510, 410)

    def zhandou(self):
        time.sleep(3)
        self.game_tool.camera_up2(10)
        self.game_tool.keyboard_tool.keyboard_press_once(keyboard_map["tab"])
        cnt = 0
        cishu = 0
        while cnt < 15:
            time.sleep(0.3)
            cishu += 1
            if not self.game_tool.is_fighting():
                cnt += 1
            else:
                cnt = 0
            if cishu % 2 == 0:
                self.game_tool.keyboard_tool.keyboard_press_once(keyboard_map[kaogu_config["danti"]])
            if cishu % 5 == 0:
                self.game_tool.keyboard_tool.keyboard_press_once(keyboard_map[kaogu_config["qunti"]])
            if cishu % 12 == 0:
                self.game_tool.keyboard_tool.keyboard_press_once(keyboard_map["tab"])
            if cishu % 27 == 0:
                self.game_tool.keyboard_tool.keyboard_press_once(keyboard_map[kaogu_config["qiangyi"]])
            # 如果发现过长时间没有打完，怀疑目标被挡住
            if cishu > 150 and cishu % 50 == 0 and self.game_tool.is_block():
                # 随机选定一个方向
                dir = random.choice([(0, 100), (0, -100), (100, 0), (-100, 0)])
                for i in range(30):
                    self.game_tool.mouse_tool.left_mouse_click(center[0] + dir[0], center[1] + dir[1])
                    time.sleep(0.3)
                time.sleep(3)
                self.game_tool.keyboard_tool.keyboard_press_once(keyboard_map["tab"])
            logger.info('战斗中。。。,当前停止参数%s,战斗时间参数%s' % (cnt, cishu))
        logger.info('检测到战斗完成')

    def go_to_ceratin_place_kaogu(self):
        time.sleep(1)
        self.game_tool.mouse_tool.left_mouse_click(860, 440)
        self.game_tool.mouse_tool.left_mouse_click(860, 440)
        time.sleep(7)
        self.game_tool.location()
        logger.info('自动寻路中。。。。。')
        time.sleep(3)
        self.xunlu()
        self.game_tool.keyboard_tool.keyboard_press_once(keyboard_map[kaogu_config["qunti"]])
        self.zhandou()
        self.keyboard_tool.keyboard_press_once(keyboard_map[kaogu_config["landmark"]])
        logger.info('使用地标回去')

    def exit_event(self):
        self.exit_flag = 1

    def before_kaogu(self):
        # 考古开始之前检测是否在战斗状态，如果是，就说明没有出来，就要出来
        if self.game_tool.is_fighting():
            while self.game_tool.is_fighting():
                time.sleep(0.1)
                self.game_tool.keyboard_tool.keyboard_press_once(keyboard_map[kaogu_config["danti"]])
            self.keyboard_tool.keyboard_press_once(keyboard_map[kaogu_config["landmark"]])
            logger.info('使用地标回去')
        # 还原相机初始位置
        self.game_tool.camera_down()

    def find_certain_task(self):
        logger.info('寻找相关任务。。。。。。')
        self.game_tool.find_npc_zhou()
        logger.info('找到周莲香npc')
        self.game_tool.get_task()
        logger.info('接取考古任务完成')
        time.sleep(0.5)
        # 打开任务栏
        time.sleep(2)
        self.game_tool.open_task_set()
        time.sleep(0.5)
        if self.game_tool.is_certain_task():
            logger.info('搜索成功')
            return True
        else:
            self.game_tool.give_up_task()
            logger.info('放弃任务')
            # 递归
            time.sleep(1)
            self.find_certain_task()
        return False

    def kaogu(self):
        self.before_kaogu()
        self.game_tool.put_things_to_repo(pkg_num=2, from_cell_num=25, to_cell_num=35)
        self.keyboard_tool.keyboard_press_once(keyboard_map[kaogu_config["bianshen"]])
        time.sleep(1)
        # if not self.game_tool.is_caishen():
        #     print("你没财神了，吃财神")
        #     time.sleep(3)
        #     self.keyboard_tool.keyboard_press_once(keyboard_map[kaogu_config["caishen"]])
        #     time.sleep(1)
        if not self.game_tool.is_sudu():
            print("你没速度了，吃速度")
            time.sleep(2)
            self.keyboard_tool.keyboard_press_once(keyboard_map[kaogu_config["sudu"]])
            time.sleep(1)
        time.sleep(3)
        # self.game_tool.camera_up(40)
        self.find_certain_task()
        self.game_tool.camera_down()
        self.go_to_certain_place()
        self.go_to_ceratin_place_kaogu()

    def run(self):
        cnt = 1
        while True:
            time.sleep(8)
            logger.info('-' * 50)
            logger.info('正在执行第' + str(cnt) + '次考古')
            self.kaogu()
            logger.info('第' + str(cnt) + '次考古完成')
            cnt += 1


def kaogu(hwnd):
    pythoncom.CoInitialize()
    wabao = WaBao(hwnd)
    wabao.run()
