# load UI
import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

from face.activation_monitor import Ui_MainWindow

category_header = {"Granite": "Q", "BlueBerry": "Q", "Lumber": "Q", "Angel": "A", "Syrup": "Y"}
mac_type = {"GFC-UP": "GU", "GFC-DOWN": "GD"}
mac_no = 60


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.category = self.category_select.currentText().split("-")[0]
        self.mac_type = self.mac_type_select.currentText()
        self.add_all_activation()

    def add_all_activation(self):
        for i in range(1, mac_no - 1):
            mac_name = QLabel("%s%s" % (category_header[self.category], mac_type[self.mac_type] + str(i).zfill(2) + "XX"))
            mac_name.setMinimumSize(QtCore.QSize(0, 50))
            self.gridLayout.addWidget(mac_name, i, 0, 1, 1)

            activation_status = QLabel(self.scrollAreaWidgetContents)
            self.gridLayout.addWidget(activation_status, i, 1, 1, 1)

            activation_val = QLabel(self.scrollAreaWidgetContents)
            self.gridLayout.addWidget(activation_val, i, 2, 1, 1)


app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()

sys.exit(app.exec_())
