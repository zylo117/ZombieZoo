# load UI
import datetime
import sys
import numpy as np
import pandas as pd

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
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
        self.activation_val_list = []

        self.data_loaded = False
        self.gfc_data = None

        # init
        self.update_date()
        self.add_all_activation()

        self.category_select.currentIndexChanged.connect(lambda x: self.change_all_activation())
        self.mac_type_select.currentIndexChanged.connect(lambda x: self.change_all_activation())

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
            self.activation_status_list.append(activation_status)

            activation_val = QLabel()
            activation_val.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            activation_val.setText("0 % ")
            self.gridLayout.addWidget(activation_val, i, 2, 1, 1)
            self.activation_val_list.append(activation_val)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 9)
        self.gridLayout.setColumnStretch(2, 1)

    def change_all_activation(self):
        self.config = self.category_select.currentText()
        self.category = self.config.split("-")[0]
        self.mac_type = self.mac_type_select.currentText()
        for i in range(mac_no_total):
            self.mac_name_list[i].setText(
                "%s%s" % (category_header[self.category], mac_type[self.mac_type] + str(i + 1).zfill(2) + "XX"))
            self.mac_name_list[i].setHidden(False)
            self.activation_status_list[i].setHidden(False)
            self.activation_val_list[i].setHidden(False)

    def show_act_val(self, manual=False):
        if not self.data_loaded:
            self.gfc_data = pd.read_csv(default_gfc_data_csv_path)
            self.data_loaded = True

        if manual:
            from_time = self.from_time.dateTime().toString(Qt.ISODate).replace("T", " ")
            to_time = self.to_time.dateTime().toString(Qt.ISODate).replace("T", " ")

            act_result = cal_act(self.gfc_data, from_time, to_time, category=self.config)
        else:
            self.gfc_data = pd.read_csv(default_gfc_data_csv_path)
            act_result = cal_act(self.gfc_data, category=self.config)

        for i in range(mac_no_total):
            try:
                activation = act_result["%s%s" % (category_header[self.category], mac_type[self.mac_type] + str(i + 1).zfill(2) + "XX")]
                activation = str(np.round(activation * 100, 2)) + " % "
                self.activation_val_list[i].setText(activation)
            except:
                self.mac_name_list[i].setHidden(True)
                self.activation_status_list[i].setHidden(True)
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

app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()

sys.exit(app.exec_())
