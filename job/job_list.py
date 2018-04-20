import time
import numpy as np

import pyautogui

import zombie.program_operation as program
import zombie.window_operation as window
import zombie.fake_input as input


def open_pg(program_path):
    # check if window is opened
    mes_main_window = window.Window("羽冠计算机")
    if mes_main_window.handle_of_window != 0:
        # if so, close it
        print("Program is running, closing it")
        program.Program("taskkill /im MDIMain.exe /f ").run()

    program.Program(program_path).run()
    while True:
        mes_main_window = window.Window("羽冠计算机")
        if mes_main_window.handle_of_window == 0:
            print("waiting for window open")
            time.sleep(3)
        else:
            print("window opened")
            break


def login(user_name, password):
    while True:
        mes_login = window.Window("登入")
        if mes_login.handle_of_window == 0:
            print("waiting for login window")
            time.sleep(1)
        else:
            print("Ready to operate")
            break
    mes_login.bring_to_top()

    print("Entering Username")
    input.key_input(user_name)

    input.function_key_input("tab")

    print("Entering Password")
    input.key_input(password)

    input.function_key_input("enter")

    while True:
        mes_logged_window = window.Window("羽冠计算机(正式区)")
        if mes_logged_window.handle_of_window == 0:
            print("logging in")
            time.sleep(2)
        else:
            print("MES login succeed")
            break


def get_gfc_lot_data(process, procedure, from_time, to_time, save_path, interval=1):
    # select Find
    pyautogui.click(430, 40)
    time.sleep(interval)
    # select process output
    for i in range(4):
        pyautogui.press("down")
    pyautogui.press("enter")

    # select process
    pyautogui.click(20, 110)
    time.sleep(interval)
    pyautogui.click(168, 110)
    time.sleep(interval)
    # enter process code
    pyautogui.typewrite(process)
    time.sleep(interval * 2)
    pyautogui.press("enter")
    time.sleep(interval)
    # select procedure
    pyautogui.click(20, 138)
    time.sleep(interval)
    pyautogui.click(180, 136)
    time.sleep(interval)
    pyautogui.typewrite(procedure)
    time.sleep(interval)
    pyautogui.press("enter")
    time.sleep(interval)

    # parse time
    from_time = from_time.split("/")
    to_time = to_time.split("/")

    # enter from_time
    pyautogui.click(548, 108)
    time.sleep(interval)
    pyautogui.typewrite(from_time[0])
    time.sleep(interval)
    pyautogui.click(574, 108)
    pyautogui.typewrite(from_time[1])
    time.sleep(interval)
    pyautogui.click(594, 108)
    pyautogui.typewrite(from_time[2])
    time.sleep(interval)
    pyautogui.click(612, 108)
    pyautogui.typewrite(from_time[3])
    time.sleep(interval)
    pyautogui.click(628, 108)
    pyautogui.typewrite(from_time[4])
    time.sleep(interval)
    pyautogui.click(644, 108)
    pyautogui.typewrite(from_time[5])
    time.sleep(interval)

    # enter to_time
    pyautogui.click(782, 108)
    pyautogui.typewrite(to_time[0])
    time.sleep(interval)
    pyautogui.click(804, 108)
    pyautogui.typewrite(to_time[1])
    time.sleep(interval)
    pyautogui.click(824, 108)
    pyautogui.typewrite(to_time[2])
    time.sleep(interval)
    pyautogui.click(840, 108)
    pyautogui.typewrite(to_time[3])
    time.sleep(interval)
    pyautogui.click(856, 108)
    pyautogui.typewrite(to_time[4])
    time.sleep(interval)
    pyautogui.click(872, 108)
    pyautogui.typewrite(to_time[5])
    time.sleep(interval)

    # start searching
    pyautogui.press("f8")
    # test if it's done searching
    while True:
        time.sleep(1)
        screen = pyautogui.screenshot()
        screen = screen.crop((100, 300, 200, 400))
        screen = np.asarray(screen)
        mean = np.mean(screen)
        if mean < 255:
            break

    # save result
    time.sleep(interval)
    pyautogui.rightClick(120, 480)
    # save as csv
    pyautogui.press("down")
    pyautogui.press("down")
    pyautogui.press("down")
    pyautogui.press("down")
    pyautogui.press("enter")
    time.sleep(interval)
    # enter save path
    pyautogui.typewrite(save_path)
    pyautogui.press("enter")
    time.sleep(interval)
    pyautogui.typewrite("y")
    time.sleep(interval)
    pyautogui.press("enter")
    time.sleep(interval)
    pyautogui.press("esc")
    time.sleep(interval)
    pyautogui.press("enter")


if __name__ == "__main__":
    program_path = "../target_program/MES/StartCenter.exe"
    open_pg(program_path)
    login("5117006014", "oit")
    get_gfc_lot_data("GFCUP", "GFC-UP", "2018/04/19/01/01/01", "2018/04/20/01/01/01", "c:\\temp\\fuck.csv", interval=0.5)
