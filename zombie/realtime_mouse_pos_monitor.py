import os, time
import pyautogui as pag

old_x = 0
old_y = 0
while True:
    x, y = pag.position()  # 返回鼠标的坐标
    if x == old_x and old_y == y:
        continue
    old_x = x
    old_y = y
    posStr = "Position:" + str(x) + ',' + str(y)
    print(posStr)  # 打印坐标
    time.sleep(0.2)
