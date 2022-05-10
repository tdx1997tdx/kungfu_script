import win32com.client
import time

dm = win32com.client.Dispatch('dm.dmsoft')
print("防锁屏启动")
while 1:
    dm.MoveTo(100, 100)
    dm.MoveTo(200, 200)
    time.sleep(1800)
