from event import *
import pythoncom
from game_config import *


def shuaguai(hwnd):
    pythoncom.CoInitialize()
    event_list = []
    event_list.append(KeyBoardEvent(hwnd, press_config["wu_hu_qiang"], 0.5))
    event_list.append(KeyBoardEvent(hwnd, 'tab', 5))
    event_list.append(KeyBoardEvent(hwnd, 'f11', 120))
    event_list.append(KeyBoardEvent(hwnd, 'f12', 120))
    event_list.append(MonitorDrugEvent(hwnd, drug_config["yuzhi"], drug_config["drug_hotkey"]))
    for i in event_list:
        i.start()
    while 1:
        time.sleep(10)
