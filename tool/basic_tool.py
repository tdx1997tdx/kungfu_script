import win32com.client


class KeyboardTool:
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.dm = win32com.client.Dispatch('dm.dmsoft')
        self.dm.BindWindow(hwnd, "normal", "windows", "windows", 0)

    # 持续按压键盘
    def keyboard_keep_press(self, key_code):
        self.dm.KeyDown(key_code)

    # 释放键盘
    def keyboard_release(self, key_code):
        self.dm.KeyUp(key_code)

    # 点击键盘
    def keyboard_press_once(self, key_code):
        self.dm.KeyPress(key_code)


class MouseTool:
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.dm = win32com.client.Dispatch('dm.dmsoft')
        self.dm.BindWindow(hwnd, "normal", "windows", "windows", 0)

    # 获取鼠标当前的hwnd
    def get_mouse_hwnd(self):
        hwnd = self.dm.GetMousePointWindow()
        self.dm.LeftDown()

    # 左键连续按压
    def left_mouse_keep_press(self, x, y):
        self.dm.MoveTo(x, y)
        self.dm.LeftDown()

    # 左键连续按压
    def left_mouse_realse(self):
        self.dm.LeftUp()

    # 左键点击
    def left_mouse_click(self, x, y):
        self.dm.MoveTo(x, y)
        self.dm.LeftClick()

    # 左键双击
    def double_click(self, x, y):
        self.dm.MoveTo(x, y)
        self.dm.LeftDoubleClick()
        # self.left_mouse_click(x, y)
        # time.sleep(0.1)
        # self.left_mouse_click(x, y)

    # 右键点击
    def right_mouse_click(self, x, y):
        self.dm.MoveTo(x, y)
        self.dm.RightClick()

    # 鼠标移动
    def mouse_move(self, x, y):
        self.dm.MoveTo(x, y)

    # 鼠标拖动
    def drag(self, x1, y1, x2, y2):
        self.left_mouse_keep_press(x1, y1)
        self.dm.MoveTo(x2, y2)
        self.dm.LeftUp()

    # 滚轮向上
    def wheel_up(self, step):
        for i in range(step):
            self.dm.WheelUp()

    # 滚轮向下
    def wheel_down(self, step):
        for i in range(step):
            self.dm.WheelDown()


class ImageTool:
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.dm = win32com.client.Dispatch('dm.dmsoft')
        self.dm.BindWindow(hwnd, "dx2", "windows", "windows", 0)

    def find_img(self, img_src, x1=0, y1=0, x2=1028, y2=800, sim=0.8):
        dm_ret = self.dm.FindPic(x1, y1, x2, y2, img_src, "000000", sim, 0)
        return dm_ret

    def screen_shot(self, x1, y1, x2, y2, file_name):
        ret = self.dm.Capture(x1, y1, x2, y2, file_name)

    def certain_place_is_change(self, x1, y1, x2, y2, t):
        res = self.dm.IsDisplayDead(x1, y1, x2, y2, t)
        return True if res == 0 else False

    def find_str(self, s, src, x1=0, y1=0, x2=1028, y2=800, sim=0.8):
        self.dm.setDict(0, src)
        self.dm.useDict(0)
        dm_ret = self.dm.FindStr(x1, y1, x2, y2, s, "000000-000000", sim)
        return dm_ret

    def get_color(self, x,y):
        dm_ret = self.dm.GetColor(x,y)
        return dm_ret


class MemTool:
    def __init__(self, hwnd):
        self.hwnd = hwnd
        self.dm = win32com.client.Dispatch('dm.dmsoft')

    # 读取内存数据
    def read_str(self, addr, len):
        self.dm.ReadData(self.hwnd, addr, len)

    # 读取内存数据
    def read_int(self, addr, type):
        self.dm.ReadInt(self.hwnd, addr, type)

    # 读取内存数据
    def read_float(self, addr):
        self.dm.ReadFloat(self.hwnd, addr)
