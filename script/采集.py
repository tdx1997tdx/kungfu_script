from event import *
import pythoncom
import random

zuobiao = [
    ((109, 285), 1),
    ((129, 320), 2),
    ((113, 366), 3),
    ((70, 393), 3),
    ((111, 387), 1),
    ((83, 424), 2),
    ((128, 428), 2),
    ((145, 473), 2),
    ((112, 507), 2),
    ((96, 527), 2),
    ((153, 414), 3),
    ((184, 454), 1),
    ((186, 404), 2),
    ((222, 435), 2),
    ((211, 394), 3),
    ((196, 366), 1),
    ((293, 313), 3),
    ((303, 337), 2),
    ((263, 433), 3),
    ((293, 397), 2),
    ((315, 419), 2),
    ((301, 454), 3),
    ((317, 483), 1),
    ((382, 480), 2),
    ((412, 442), 3),
    ((398, 407), 1),
    ((433, 408), 3),
    ((445, 405), 2),
    ((436, 394), 3),
    ((420, 361), 2),
    ((440, 346), 1),
    ((398, 330), 3),
    ((401, 314), 3),
    ((400, 276), 1),
    ((402, 263), 1),
    ((455, 259), 1),
    ((415, 231), 3),
    ((518, 217), 3),
    ((511, 192), 1),
    ((549, 225), 1),
    ((561, 217), 1),
    ((541, 185), 2),
    ((555, 189), 3),
    ((603, 172), 3),
    ((623, 146), 1),
    ((694, 145), 2),
    ((714, 194), 3),
    ((721, 147), 1),
    ((754, 167), 1),
    ((734, 196), 1),
    ((711, 220), 1),
    ((669, 214), 1)
]


def caiji(hwnd):
    pythoncom.CoInitialize()
    t1 = MonitorStopEvent(hwnd)
    t1.start()
    keyboard_tool = KeyboardTool(hwnd)
    mouse_tool = MouseTool(hwnd)
    game_tool = KungfuGameTool(hwnd)
    while 1:
        for elem in zuobiao:
            time.sleep(1)
            if elem[1] not in [1, 2, 3]:
                continue
            print(elem)
            keyboard_tool.keyboard_press_once(keyboard_map['m'])
            time.sleep(1)
            mouse_tool.left_mouse_click(786, 14)
            time.sleep(0.1)
            for i in range(35):
                mouse_tool.left_mouse_click(917, 630)
                time.sleep(0.1)
            time.sleep(0.3)
            mouse_tool.double_click(*elem[0])
            time.sleep(1)
            keyboard_tool.keyboard_press_once(keyboard_map['m'])
            cnt = 0
            while cnt < 5:
                if t1.is_stop:
                    cnt += 1
                else:
                    cnt = 0
                logger.info('自动寻路中。。。。。,当前停止参数%s' % (cnt))
                time.sleep(0.5)
            logger.info('寻路结束')
            game_tool.camera_up(40)
            time.sleep(0.5)
            mouse_tool.left_mouse_click(580, 13)
            time.sleep(0.5)
            x1, y1 = 156, 105
            heng = 18
            zong = 12
            finalx, finaly = None, None
            for i in range(heng):
                for j in range(zong):
                    t_x = x1 + i * 38
                    t_y = y1 + j * 38
                    mouse_tool.double_click(t_x, t_y)
                    time.sleep(0.02)
                    is_ok = game_tool.is_zaiwa()
                    if is_ok:
                        finalx, finaly = t_x, t_y
                        logger.info('找到采集物品坐标:%s,%s' % (finalx, finaly))
                        break
                if finalx:
                    break
            if finalx:
                logger.info('开挖')
                mouse_tool.double_click(finalx, finaly)
                cnt = 0
                while cnt < 40:
                    r_x = int((random.random() - 0.5) * 80)
                    r_y = int((random.random() - 0.5) * 80)
                    mouse_tool.double_click(finalx + r_x, finaly + r_y)
                    time.sleep(0.1)
                    cnt += 1
                s = time.time()
                time.sleep(8)
                print("进入读秒")
                while 1:
                    if not game_tool.is_zaiwa() or time.time() - s > 18:
                        break
                    time.sleep(0.5)
            else:
                logger.info("没找到东西啊")
            logger.info('采集完成')
            game_tool.camera_down()
        # 回到石头那边传送回去
        keyboard_tool.keyboard_press_once(keyboard_map['m'])
        time.sleep(1)
        mouse_tool.left_mouse_click(786, 14)
        time.sleep(0.1)
        for i in range(35):
            mouse_tool.left_mouse_click(917, 630)
            time.sleep(0.1)
        time.sleep(0.3)
        mouse_tool.double_click(607, 131)
        time.sleep(1)
        keyboard_tool.keyboard_press_once(keyboard_map['m'])
        cnt = 0
        while cnt < 5:
            if t1.is_stop:
                cnt += 1
            else:
                cnt = 0
            logger.info('自动寻路中。。。。。,当前停止参数%s' % (cnt))
            time.sleep(0.5)
        logger.info('寻路结束')
        x, y = game_tool.chuansong()
        mouse_tool.left_mouse_click(x, y)
        time.sleep(0.3)
        mouse_tool.left_mouse_click(473, 360)
