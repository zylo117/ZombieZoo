import subprocess

from zombie.window_operation import Window


class Program:
    def __init__(self, program_path):
        self.path = program_path

    def run(self):
        subprocess.Popen(self.path)


if __name__ == "__main__":
    pg = Program("explorer.exe")
    pg.run()

    mes_main_window = Window("Github")
    mes_main_window.list_all_windows(printout=True)
