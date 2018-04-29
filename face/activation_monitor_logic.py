# load UI
import cv2
import datetime
import sys
import numpy as np
import pandas as pd

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

from face.activation_monitor import Ui_MainWindow
from brain.gfc_activation_calculator import cal_act

category_header = {"Granite": "Q",
                   "BlueBerry": "Q",
                   "Lumber": "H",
                   "Angel": "A",
                   "Syrup": "Y"}
mac_type = {"GFC-UP": "GU", "GFC-DOWN": "GD",
            "OQC-UP": "QU", "OQC-DOWN": "QD",
            "CUBE-UP": "CU", "CUBE-DOWN": "CD",
            "REL-UP": "RU", "REL-DOWN": "RD"}
mac_no_total = 60
default_gfc_data_csv_path = "F:/Document/GitHub/ZombieZoo/face/000.csv"
from_time = "2018/04/28 12:50:50"
to_time = "2018/04/28 18:50:50"


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.config = self.category_select.currentText()
        self.category = self.config.split("-")[0]
        self.mac_type = self.mac_type_select.currentText()
        self.mac_name_list = []
        self.activation_status_list = []
        self.yield_val_list = []
        self.activation_val_list = []

        self.data_loaded = False
        self.gfc_data = None

        # init
        self.update_date()
        self.add_all_activation()

        self.category_select.currentIndexChanged.connect(lambda x: self.show_all_activation())
        self.mac_type_select.currentIndexChanged.connect(lambda x: self.show_all_activation())

        # buttons events
        self.auto_load_data.clicked.connect(lambda x: self.show_act_val())
        self.manual_load_data.clicked.connect(lambda x: self.show_act_val(manual=True))
        self.reload.clicked.connect(self.reload_data)

    def add_all_activation(self):
        for i in range(mac_no_total):
            mac_name = QLabel()
            mac_name.setText("%s%s" % (category_header[self.category], mac_type[self.mac_type] + str(i + 1).zfill(2) + "XX"))
            mac_name.setMinimumSize(QtCore.QSize(0, 50))
            self.gridLayout.addWidget(mac_name, i, 0, 1, 1)
            self.gridLayout.setColumnStretch(0, 1)
            self.mac_name_list.append(mac_name)

            activation_status = QLabel()
            self.gridLayout.addWidget(activation_status, i, 1, 1, 1)
            activation_status.setScaledContents(True)
            self.activation_status_list.append(activation_status)

            yield_val = QLabel()
            yield_val.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            yield_val.setText("0 % ")
            self.gridLayout.addWidget(yield_val, i, 2, 1, 1)
            self.yield_val_list.append(yield_val)

            activation_val = QLabel()
            activation_val.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            activation_val.setText("0 % ")
            self.gridLayout.addWidget(activation_val, i, 3, 1, 1)
            self.activation_val_list.append(activation_val)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 9)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)

    def show_all_activation(self):
        self.config = self.category_select.currentText()
        self.category = self.config.split("-")[0]
        self.mac_type = self.mac_type_select.currentText()
        for i in range(mac_no_total):
            self.mac_name_list[i].setText(
                "%s%s" % (category_header[self.category], mac_type[self.mac_type] + str(i + 1).zfill(2) + "XX"))
            self.mac_name_list[i].setHidden(False)
            self.activation_status_list[i].setHidden(False)
            self.yield_val_list[i].setHidden(False)
            self.activation_val_list[i].setHidden(False)

    def show_act_val(self, manual=False):
        self.show_all_activation()

        if not self.data_loaded:
            self.gfc_data = pd.read_csv(default_gfc_data_csv_path)
            self.data_loaded = True

        if manual:
            from_time = self.from_time.dateTime().toString(Qt.ISODate).replace("T", " ")
            to_time = self.to_time.dateTime().toString(Qt.ISODate).replace("T", " ")

            self.from_time_stamp.setText(":".join(from_time.split(" ")[1].split(":")[:2]))
            to_time_stamp = ":".join(to_time.split(" ")[1].split(":")[:2])
            if to_time_stamp == "00:00":
                to_time_stamp = "24:00"
            self.to_time_stamp.setText(to_time_stamp)

            yield_vals, act_vals, act_pics = cal_act(self.gfc_data, from_time, to_time, category=self.config)
        else:
            self.gfc_data = pd.read_csv(default_gfc_data_csv_path)
            yield_vals, act_vals, act_pics = cal_act(self.gfc_data, category=self.config)

        for i in range(mac_no_total):
            try:
                yield_val = yield_vals["%s%s" % (category_header[self.category], mac_type[self.mac_type] + str(i + 1).zfill(2) + "XX")]
                yield_val = str(np.round(yield_val * 100, 2)) + " % "

                act_val = act_vals["%s%s" % (category_header[self.category], mac_type[self.mac_type] + str(i + 1).zfill(2) + "XX")]
                act_val = str(np.round(act_val * 100, 2)) + " % "

                act_pic = act_pics["%s%s" % (category_header[self.category], mac_type[self.mac_type] + str(i + 1).zfill(2) + "XX")]
                act_pic = cv2.resize(act_pic, (800, 10))
                height, width, channel = act_pic.shape
                pile_width = channel * width
                act_pic = cv2.cvtColor(act_pic, cv2.COLOR_BGR2RGB)
                q_image = QImage(act_pic.data, width, height, pile_width, QImage.Format_RGB888)

                self.yield_val_list[i].setText(yield_val)
                self.activation_val_list[i].setText(act_val)
                self.activation_status_list[i].setPixmap(
                    QPixmap.fromImage(q_image).scaled(self.activation_status_list[i].width(), self.activation_status_list[i].height()))
            except:
                self.mac_name_list[i].setHidden(True)
                self.activation_status_list[i].setHidden(True)
                self.yield_val_list[i].setHidden(True)
                self.activation_val_list[i].setHidden(True)
                continue

    def reload_data(self):
        self.gfc_data = pd.read_csv(default_gfc_data_csv_path)
        self.data_loaded = True

    def update_date(self):
        # # get current date and time
        # now = QtCore.QDateTime.currentDateTime()
        # # set date only
        # today = QtCore.QDate.currentDate()
        # # set time only
        # this_moment = QtCore.QTime.currentTime()
        # # set an arbitrary date
        # some_date = QtCore.QDate(2011, 4, 22)  # Year, Month, Day
        # # set an arbitrary time
        # some_time = QtCore.QTime(16, 33, 15)  # Hours, Minutes, Seconds (Only H and M required)
        # # set an arbitrary date and time
        # someDT = QtCore.QDateTime(2011, 4, 22, 16, 33, 15)

        from_time = datetime.datetime.strptime(str(datetime.date.today()) + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        to_time = datetime.datetime.strptime(str(datetime.date.today() + datetime.timedelta(days=1)) + " 00:00:00", "%Y-%m-%d %H:%M:%S")

        self.from_time.setDateTime(from_time)
        self.to_time.setDateTime(to_time)

    def generate_color_bar(self, time_data):
        print(0)

app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()

sys.exit(app.exec_())
