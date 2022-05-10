from script.刷boss import shuaboss
from script.采集 import caiji
from script.刷怪 import shuaguai
from script.考古 import kaogu
from script.工匠 import gongjiang
from event import *
import pythoncom
import multiprocessing
import keyboard
from process_dict import *


def begin_shuaboss():
    pythoncom.CoInitialize()
    dm = win32com.client.Dispatch('dm.dmsoft')
    hwnd = dm.GetMousePointWindow()
    mp = multiprocessing.Process(target=shuaboss, args=(hwnd,))
    mp.start()
    add(hwnd, mp.pid)
    logger.info("开始刷boss")


def begin_caiji():
    pythoncom.CoInitialize()
    dm = win32com.client.Dispatch('dm.dmsoft')
    hwnd = dm.GetMousePointWindow()
    mp = multiprocessing.Process(target=caiji, args=(hwnd,))
    mp.start()
    add(hwnd, mp.pid)
    logger.info("开始采集")


def begin_shuaguai():
    pythoncom.CoInitialize()
    dm = win32com.client.Dispatch('dm.dmsoft')
    hwnd = dm.GetMousePointWindow()
    mp = multiprocessing.Process(target=shuaguai, args=(hwnd,))
    mp.start()
    add(hwnd, mp.pid)
    logger.info("开始刷怪")


def begin_wabao():
    pythoncom.CoInitialize()
    dm = win32com.client.Dispatch('dm.dmsoft')
    hwnd = dm.GetMousePointWindow()
    mp = multiprocessing.Process(target=kaogu, args=(hwnd,))
    mp.start()
    add(hwnd, mp.pid)
    logger.info("开始考古")


def begin_gongjiang():
    pythoncom.CoInitialize()
    dm = win32com.client.Dispatch('dm.dmsoft')
    hwnd = dm.GetMousePointWindow()
    mp = multiprocessing.Process(target=gongjiang, args=(hwnd,))
    mp.start()
    add(hwnd, mp.pid)
    logger.info("开始工匠")


def kill():
    pythoncom.CoInitialize()
    dm = win32com.client.Dispatch('dm.dmsoft')
    hwnd = dm.GetMousePointWindow()
    delete(hwnd)


if __name__ == '__main__':
    print("欢迎")
    keyboard.add_hotkey('ctrl+;', begin_caiji)
    keyboard.add_hotkey('ctrl+\'', begin_shuaboss)
    keyboard.add_hotkey('ctrl+m', begin_shuaguai)
    keyboard.add_hotkey('ctrl+/', begin_wabao)
    keyboard.add_hotkey('ctrl+n', begin_gongjiang)
    keyboard.add_hotkey('ctrl+.', kill)
    keyboard.wait()
