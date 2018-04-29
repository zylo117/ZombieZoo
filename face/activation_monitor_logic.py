# load UI
import sys
import numpy as np

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

from face.activation_monitor import Ui_MainWindow
from brain.gfc_activation_calculator import cal_act

category_header = {"Granite": "Q", "BlueBerry": "Q", "Lumber": "H", "Angel": "A", "Syrup": "Y"}
mac_type = {"GFC-UP": "GU", "GFC-DOWN": "GD"}
mac_no_total = 60
default_gfc_data_csv_path = "F:/Document/GitHub/ZombieZoo/face/000.csv"
from_time = "2018/04/28 12:50:50"
to_time = "2018/04/28 18:50:50"

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.category = self.category_select.currentText().split("-")[0]
        self.mac_type = self.mac_type_select.currentText()
        self.mac_name_list = []
        self.activation_status_list = []
        self.activation_val_list = []

        self.add_all_activation()

        self.category_select.currentIndexChanged.connect(lambda x: self.change_all_activation())

        self.auto_load_data.clicked.connect(lambda x: self.show_act_val())
        self.manual_load_data.clicked.connect(lambda x: self.show_act_val(manual=True))

    def add_all_activation(self):
        for i in range(mac_no_total):
            mac_name = QLabel("%s%s" % (category_header[self.category], mac_type[self.mac_type] + str(i + 1).zfill(2) + "XX"))
            mac_name.setMinimumSize(QtCore.QSize(0, 50))
            self.gridLayout.addWidget(mac_name, i, 0, 1, 1)
            self.gridLayout.setColumnStretch(0, 1)
            self.mac_name_list.append(mac_name)

            activation_status = QLabel(self.scrollAreaWidgetContents)
            self.gridLayout.addWidget(activation_status, i, 1, 1, 1)
            self.activation_status_list.append(activation_status)

            activation_val = QLabel(self.scrollAreaWidgetContents)
            activation_val.setAlignment(QtCore.Qt.AlignVCenter|QtCore.Qt.AlignRight)
            activation_val.setText("0 % ")
            self.gridLayout.addWidget(activation_val, i, 2, 1, 1)
            self.activation_val_list.append(activation_val)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 9)
        self.gridLayout.setColumnStretch(2, 1)


    def change_all_activation(self):
        self.category = self.category_select.currentText().split("-")[0]
        self.mac_type = self.mac_type_select.currentText()
        for i in range(mac_no_total):
            self.mac_name_list[i].setText(
                "%s%s" % (category_header[self.category], mac_type[self.mac_type] + str(i + 1).zfill(2) + "XX"))

    def show_act_val(self, manual=False):
        if manual:
            from_time = self.from_time.dateTime().toString(Qt.ISODate).replace("T", " ")
            to_time = self.to_time.dateTime().toString(Qt.ISODate).replace("T", " ")

            act_result = cal_act(default_gfc_data_csv_path, from_time, to_time)
        else:
            act_result = cal_act(default_gfc_data_csv_path)

        for i in range(mac_no_total):
            try:
                activation = act_result["%s%s" % (category_header[self.category], mac_type[self.mac_type] + str(i + 1).zfill(2) + "XX")]
                activation = str(np.round(activation * 100, 2)) + " % "
                self.activation_val_list[i].setText(activation)
            except:
                continue

app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()

sys.exit(app.exec_())
