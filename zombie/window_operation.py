#! /usr/bin/env python
# -*- coding: utf-8 -*-
import win32gui
import win32api

import win32con


class Window:
    def __init__(self, window_name):
        self.current_windows_list = set()

        # define window by its name
        self.window_name = window_name
        self.handle_of_window = win32gui.FindWindow(None, self.window_name)

        # if window name doesn't match but it's window name's prefix, then start prefix matching
        if self.handle_of_window == 0:
            windows_list = self.list_all_windows(printout=False)
            for title in windows_list:
                if str(title).__contains__(window_name):
                    self.window_name = title
                    break
            # define window by its name
            self.handle_of_window = win32gui.FindWindow(None, self.window_name)

        if self.handle_of_window == 0:
            # print("Target window is not found")
            return

        # get window current position
        self.x = None
        self.y = None
        self.width = None
        self.height = None
        self.get_pos()

        # get sys current resolution
        self.sys_resolution = self.get_sys_resolution()

    def get_sys_resolution(self):
        width = win32api.GetSystemMetrics(0)
        height = win32api.GetSystemMetrics(1)
        return width, height

    def bring_to_top(self):
        win32gui.SetForegroundWindow(self.handle_of_window)

    def maximize(self):
        win32gui.SendMessage(self.handle_of_window, win32con.WM_SYSCOMMAND, win32con.SC_MAXIMIZE, 0)

    def un_maximize(self):
        win32gui.SendMessage(self.handle_of_window, win32con.WM_SYSCOMMAND, win32con.SC_RESTORE, 0)

    def minimize(self):
        win32gui.SendMessage(self.handle_of_window, win32con.WM_SYSCOMMAND, win32con.SC_MINIMIZE, 0)

    def get_pos(self):
        left, top, right, bottom = win32gui.GetWindowRect(self.handle_of_window)
        self.x = left
        self.y = top
        self.width = right - left
        self.height = bottom - top

    def move_windows(self, x, y, resize=False, repaint=False):
        if resize:
            win32gui.MoveWindow(self.handle_of_window, x, y, resize[0], resize[1], repaint)
        else:
            win32gui.MoveWindow(self.handle_of_window, x, y, self.width, self.height, repaint)

        self.get_pos()

    def close(self):
        win32gui.PostMessage(self.handle_of_window, win32con.WM_CLOSE, 0, 0)

    def _list_all_windows(self, hwnd, mouse):
        """
        IsWindow(hwnd): hwnd is window
        IsWindowEnabled(hwnd): hwnd is enable
        IsWindowVisible(hwnd):hwnd is visible, multi-tabs that don't show is considered as disable
        :param hwnd:
        :param mouse:
        :return:
        """

        # if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
        if win32gui.IsWindow(hwnd) and win32gui.IsWindowEnabled(hwnd):
            self.current_windows_list.add(win32gui.GetWindowText(hwnd))

    def list_all_windows(self, printout=True):
        """
        list all windows, including children windows under parent windows
        :param printout:
        :return:
        """
        win32gui.EnumWindows(self._list_all_windows, 0)
        lt = [t for t in self.current_windows_list if t]
        lt.sort()

        if printout:
            for t in lt:
                print(t)

        return lt


if __name__ == "__main__":
    import time
    window = Window("羽冠") # support prefix auto match searching
    window.list_all_windows()
    window.move_windows(0, 0)

    window.bring_to_top()
    window.get_menu()

    # time.sleep(1)
    # window.maximize()
    # time.sleep(1)
    # window.un_maximize()
    #
    # window.list_all_windows(printout=True)
    # time.sleep(1)
    # window.minimize()

    # hwnd = win32gui.FindWindow(None, "Github")
    # win32gui.SetForegroundWindow(hwnd)
    # win32gui.MoveWindow(hwnd, 10, 10, 1200, 600, False)  # hwnd, x,y,width,height,ifRepaint

    # window.close()

    # classname = None
    # titlename = "GitHub"
    # # 获取句柄
    # hwnd = win32gui.FindWindow(classname, titlename)
    # # 获取窗口左上角和右下角坐标
    # left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    # print(left, top, right, bottom)
    #
    # #获取某个句柄的类名和标题
    # title = win32gui.GetWindowText(hwnd)
    # classname = win32gui.GetClassName(hwnd)

    # 获取父句柄hwnd类名为classname的子句柄
    # hwnd1= win32gui.FindWindowEx(hwnd, None, classname, None)
    # title = win32gui.GetWindowText(hwnd1)
    # classname = win32gui.GetClassName(hwnd1)
    # print(0)
