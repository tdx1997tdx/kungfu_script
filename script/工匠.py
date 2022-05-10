from event import *
import pythoncom
import multiprocessing
from process_dict import process_dict


def gongjiang(hwnd):
    pythoncom.CoInitialize()
    time.sleep(2)
    logger.info("自动刷生皮棉絮工匠开始")
    mt = MouseTool(hwnd)
    while True:
        mt.left_mouse_click(367, 628)
        time.sleep(0.3)
