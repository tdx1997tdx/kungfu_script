from event import *
import pythoncom
from game_config import *


def shuaboss(hwnd):
    pythoncom.CoInitialize()
    event_list = []
    event_list.append(KeyBoardEvent(hwnd, press_config["wu_hu_qiang"], 0.5))
    event_list.append(KeyBoardEvent(hwnd, press_config["qiang_yi"], 10))
    event_list.append(MonitorDrugEvent(hwnd, drug_config["yuzhi"], drug_config["drug_hotkey"]))
    for i in event_list:
        i.start()
    while 1:
        time.sleep(10)
