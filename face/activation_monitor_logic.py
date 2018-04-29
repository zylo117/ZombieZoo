# load UI
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

from face.activation_monitor import Ui_MainWindow

category_header = {"Granite": "Q", "BlueBerry": "Q", "Lumber": "H", "Angel": "A", "Syrup": "Y"}
mac_type = {"GFC-UP": "GU", "GFC-DOWN": "GD"}
mac_no_total = 60


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

    def add_all_activation(self):
        for i in range(mac_no_total):
            mac_name = QLabel(
                "%s%s" % (category_header[self.category], mac_type[self.mac_type] + str(i + 1).zfill(2) + "XX"))
            mac_name.setMinimumSize(QtCore.QSize(0, 50))
            self.gridLayout.addWidget(mac_name, i, 0, 1, 1)
            self.mac_name_list.append(mac_name)

            activation_status = QLabel(self.scrollAreaWidgetContents)
            self.gridLayout.addWidget(activation_status, i, 1, 1, 1)
            self.activation_status_list.append(activation_status)

            activation_val = QLabel(self.scrollAreaWidgetContents)
            self.gridLayout.addWidget(activation_val, i, 2, 1, 1)
            self.activation_val_list.append(activation_val)

    def change_all_activation(self):
        self.category = self.category_select.currentText().split("-")[0]
        self.mac_type = self.mac_type_select.currentText()
        for i in range(mac_no_total):
            self.mac_name_list[i].setText(
                "%s%s" % (category_header[self.category], mac_type[self.mac_type] + str(i + 1).zfill(2) + "XX"))


app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()

sys.exit(app.exec_())
