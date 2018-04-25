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


def get_gfc_lot_data(process, procedure, from_time, to_time, category, save_path, interval=1.0):
    # select Find
    pyautogui.click(430, 40)
    time.sleep(interval)
    # select process output
    for i in range(4):
        pyautogui.press("down")
    pyautogui.press("enter")

    test_ready()

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

    # enter category
    pyautogui.click(418, 136)
    pyautogui.click(620, 136)
    pyautogui.typewrite(category)
    pyautogui.press("enter")
    time.sleep(interval)

    # start searching
    search()

    # save result
    save_data(interval, save_path)


def save_data(interval, save_path):
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
    time.sleep(interval * 4)
    pyautogui.press("enter")
    time.sleep(interval * 4)
    exit(interval)


def exit(interval):
    pyautogui.press("esc")
    time.sleep(interval * 2)
    pyautogui.press("enter")
    time.sleep(interval * 2)

def test_ready():
    # test if it's ready searching
    while True:
        time.sleep(1)
        screen = pyautogui.screenshot()
        screen = screen.crop((100, 400, 200, 500))
        screen = np.asarray(screen)
        mean = np.mean(screen)
        if mean == 255:
            break

def search():
    # start searching
    pyautogui.press("f8")
    # test if it's done searching
    while True:
        time.sleep(1)
        screen = pyautogui.screenshot()
        screen = screen.crop((100, 400, 200, 500))
        screen = np.asarray(screen)
        mean = np.mean(screen)
        if mean < 255:
            break


def get_material_data(material_code, from_time, to_time, save_path, interval=1.0):
    # select Find
    pyautogui.click(430, 40)
    time.sleep(interval)
    # select material output
    for i in range(12):
        pyautogui.press("down")
    pyautogui.press("enter")

    test_ready()

    # time
    # parse time
    from_time = from_time.split("/")
    to_time = to_time.split("/")
    # enter from_time
    pyautogui.click(156, 116)
    time.sleep(interval)
    pyautogui.typewrite(from_time[0])
    time.sleep(interval)
    pyautogui.press("right")
    pyautogui.typewrite(from_time[1])
    time.sleep(interval)
    pyautogui.press("right")
    pyautogui.typewrite(from_time[2])
    time.sleep(interval)
    pyautogui.press("right")
    pyautogui.typewrite(from_time[3])
    time.sleep(interval)
    pyautogui.press("right")
    pyautogui.typewrite(from_time[4])
    time.sleep(interval)

    # enter to_time
    pyautogui.press("tab")
    pyautogui.click(328, 116)
    pyautogui.typewrite(to_time[0])
    time.sleep(interval)
    pyautogui.press("right")
    pyautogui.typewrite(to_time[1])
    time.sleep(interval)
    pyautogui.press("right")
    pyautogui.typewrite(to_time[2])
    time.sleep(interval)
    pyautogui.press("right")
    pyautogui.typewrite(to_time[3])
    time.sleep(interval)
    pyautogui.press("right")
    pyautogui.typewrite(to_time[4])
    time.sleep(interval)

    # enter material code
    pyautogui.click(26, 148)
    time.sleep(interval)
    pyautogui.click(190, 150)
    time.sleep(interval)
    # parse material code
    code_set = ",".join(material_code)
    pyautogui.typewrite(code_set)
    time.sleep(interval)
    pyautogui.press("enter")
    time.sleep(interval)

    # click "output the maximum items"
    pyautogui.click(498, 186)
    time.sleep(interval)

    # start searching
    search()

    # save result
    save_data(interval, save_path)


if __name__ == "__main__":
    program_path = "../target_program/MES/StartCenter.exe"
    open_pg(program_path)
    login("5117006014", "oit")

    sava_path = "c:\\temp\\"  # must use "\\" instead of "/"

    get_gfc_lot_data("GFCUP", "GFC-UP", "2018/04/19/01/01/01", "2018/04/23/01/01/01", sava_path + "gfc.csv",
                     interval=0.5)

    lens_code = ["G-818-02093-GENIUS", "G-818-02093-LARGAN", "G-818-02093-OLM", "G-818-02093-KANTATSU"]
    get_material_data(lens_code, "2018/04/17/01/01/00", "2018/04/19/01/01/00", sava_path + "lens.csv", interval=0.5)

    aa_code = ["AACV125             1A", "AACV126             1A", "AACV127             1A", "AACV128             1A"]
    get_material_data(aa_code, "2018/04/17/01/01/00", "2018/04/19/01/01/00", sava_path + "aa.csv", interval=0.5)

    ircf_code = ["G-816-00424-AGC", "G-816-00424-PTOT"]
    get_material_data(ircf_code, "2018/04/17/01/01/00", "2018/04/19/01/01/00", sava_path + "ircf.csv", interval=0.5)
