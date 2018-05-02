# load UI
import cv2
import datetime
import sys
import numpy as np
import pandas as pd

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QThread, QEvent
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

from face.gfc_electrical_failure_monitor.activation_monitor import Ui_MainWindow
from face.gfc_electrical_failure_monitor.gfc_activation_calculator import cal_act

# load category data
category_header_prt = pd.read_csv("./CATEGORY.conf")
category_header_prt = [category_header_prt["key"].tolist(), category_header_prt["val"].tolist()]
category_header = {}
for i in range(len(category_header_prt[0])):
    category_header[category_header_prt[0][i].lower()] = category_header_prt[1][i]

# load machine type data
mac_type_prt = pd.read_csv("./MACTYPE.conf")
mac_type_prt = [mac_type_prt["key"].tolist(), mac_type_prt["val"].tolist()]
mac_type = {}
for i in range(len(mac_type_prt[0])):
    mac_type[mac_type_prt[0][i].lower()] = mac_type_prt[1][i]

# set max machine number
mac_no_total = 99

# set default gfc data path
default_gfc_data_csv_path = open("./DEFAULT_GFC_DATA_PATH.conf", "rb").read().decode()


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # add items
        self.mac_type_select.addItems(mac_type)
        self.mac_type_select.setCurrentIndex(0)

        self.category_select.addItems(category_header)
        self.category_select.setCurrentIndex(0)

        self.config = self.category_select.currentText().lower()
        self.mac_type = self.mac_type_select.currentText().lower()
        self.mac_name_list = []
        self.activation_status_list = []
        self.osfr_list = []
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

        # start a mouse pos monitoring thread
        app.installEventFilter(self)
        self.mouse = MousePos()
        self.mouse_window_x = 0
        self.mouse_window_y = 0
        self.mouse.start()
        self.active_labels = []

    def add_all_activation(self):
        for i in range(mac_no_total):
            mac_name = QLabel()
            mac_name.setText(
                "%s%s" % (category_header[self.config], mac_type[self.mac_type] + str(i + 1).zfill(2) + "XX"))
            mac_name.setMinimumHeight(80)
            mac_name.setMaximumHeight(160)
            self.gridLayout.addWidget(mac_name, i, 0, 1, 1)
            self.gridLayout.setColumnStretch(0, 1)
            self.mac_name_list.append(mac_name)

            activation_status = QLabel()
            activation_status.setMouseTracking(True)
            activation_status.setStatusTip("GFC Activation Status, remains developing")
            activation_status.setToolTip("DateTime")
            self.gridLayout.addWidget(activation_status, i, 1, 1, 1)
            activation_status.setScaledContents(True)
            self.activation_status_list.append(activation_status)

            osfr = QLabel()
            osfr.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            osfr.setText("0 % ")
            self.gridLayout.addWidget(osfr, i, 2, 1, 1)
            self.osfr_list.append(osfr)

            yield_val = QLabel()
            yield_val.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            yield_val.setText("0 % ")
            self.gridLayout.addWidget(yield_val, i, 3, 1, 1)
            self.yield_val_list.append(yield_val)

            activation_val = QLabel()
            activation_val.setAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
            activation_val.setText("0 % ")
            self.gridLayout.addWidget(activation_val, i, 4, 1, 1)
            self.activation_val_list.append(activation_val)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 9)
        self.gridLayout.setColumnStretch(2, 1)
        self.gridLayout.setColumnStretch(3, 1)
        self.gridLayout.setColumnStretch(4, 1)

    def show_all_activation(self):
        self.config = self.category_select.currentText().lower()
        self.mac_type = self.mac_type_select.currentText().lower()
        for i in range(mac_no_total):
            self.mac_name_list[i].setText(
                "%s%s" % (category_header[self.config], mac_type[self.mac_type] + str(i + 1).zfill(2) + "XX"))
            self.mac_name_list[i].setHidden(False)
            self.activation_status_list[i].setHidden(False)
            self.osfr_list[i].setHidden(False)
            self.yield_val_list[i].setHidden(False)
            self.activation_val_list[i].setHidden(False)

    def show_act_val(self, manual=False):
        self.show_all_activation()

        if not self.data_loaded:
            self.gfc_data = pd.read_excel(default_gfc_data_csv_path)
            self.data_loaded = True

        if manual:
            from_time = self.from_time.dateTime().toString(Qt.ISODate).replace("T", " ")
            to_time = self.to_time.dateTime().toString(Qt.ISODate).replace("T", " ")

            self.from_time_stamp.setText(":".join(from_time.split(" ")[1].split(":")[:2]))
            to_time_stamp = ":".join(to_time.split(" ")[1].split(":")[:2])
            if to_time_stamp == "00:00":
                to_time_stamp = "24:00"
            self.to_time_stamp.setText(to_time_stamp)

            yield_vals, act_vals, act_pics, osfrs = cal_act(self.gfc_data, from_time, to_time, category=self.config)
        else:
            self.gfc_data = pd.read_excel(default_gfc_data_csv_path)
            yield_vals, act_vals, act_pics, osfrs = cal_act(self.gfc_data, category=self.config)

        self.active_labels = []
        for i in range(mac_no_total):
            try:
                mac_name = "%s%s" % (category_header[self.config], mac_type[self.mac_type] + str(i + 1).zfill(2) + "XX")

                osfr = osfrs[mac_name]
                osfr = str(np.round(osfr * 100, 2)) + " % "

                yield_val = yield_vals[mac_name]
                yield_val = str(np.round(yield_val * 100, 2)) + " % "

                act_val = act_vals[mac_name]
                act_val = str(np.round(act_val * 100, 2)) + " % "

                act_pic = act_pics[mac_name]
                act_pic = cv2.resize(act_pic, (400, 1))
                height, width, channel = act_pic.shape
                pile_width = channel * width
                act_pic = cv2.cvtColor(act_pic, cv2.COLOR_BGR2RGB)
                q_image = QImage(act_pic.data, width, height, pile_width, QImage.Format_RGB888)

                self.osfr_list[i].setText(osfr)
                self.yield_val_list[i].setText(yield_val)
                self.activation_val_list[i].setText(act_val)
                self.activation_status_list[i].setPixmap(QPixmap.fromImage(q_image))

                self.active_labels.append(i)
            except:
                self.mac_name_list[i].setHidden(True)
                self.activation_status_list[i].setHidden(True)
                self.osfr_list[i].setHidden(True)
                self.yield_val_list[i].setHidden(True)
                self.activation_val_list[i].setHidden(True)
                continue

    def reload_data(self):
        self.gfc_data = pd.read_excel(default_gfc_data_csv_path)
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
        to_time = datetime.datetime.strptime(str(datetime.date.today() + datetime.timedelta(days=1)) + " 00:00:00",
                                             "%Y-%m-%d %H:%M:%S")

        self.from_time.setDateTime(from_time)
        self.to_time.setDateTime(to_time)

    # override the method to track mouse coordinates
    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseMove:
            if event.buttons() == Qt.NoButton or event.buttons() == Qt.LeftButton:
                pos = event.windowPos()
                self.mouse_window_x = pos.x()
                self.mouse_window_y = pos.y()
            else:
                pass  # do other stuff
        return QMainWindow.eventFilter(self, source, event)

    def resizeEvent(self, event):
        return QMainWindow.resizeEvent(self, event)



class MousePos(QThread):
    def __init__(self):
        super(MousePos, self).__init__()

    def run(self):
        while True:
            self.show_co()
            self.msleep(100)

    def show_co(self):
        mouse_x = mainWindow.mouse_window_x
        mouse_y = mainWindow.mouse_window_y

        # do some thing
        if len(mainWindow.active_labels) > 0:
            status_x = mainWindow.activation_status_list[mainWindow.active_labels[0]].x()
            status_y = mainWindow.activation_status_list[mainWindow.active_labels[0]].y()
            status_width = mainWindow.activation_status_list[mainWindow.active_labels[0]].width()
            status_height = mainWindow.activation_status_list[mainWindow.active_labels[0]].height()

            # calculate the factor of the current time range
            factor = (mouse_x - status_x - 10) / status_width
            if 0 < factor < 1:
                from_time = mainWindow.from_time.dateTime().toString(Qt.ISODate).replace("T", " ")
                to_time = mainWindow.to_time.dateTime().toString(Qt.ISODate).replace("T", " ")

                from_time = datetime.datetime.strptime(from_time, "%Y-%m-%d %H:%M:%S")
                to_time = datetime.datetime.strptime(to_time, "%Y-%m-%d %H:%M:%S")

                delta = (to_time - from_time) * factor
                select_time = (from_time + delta).strftime("%Y-%m-%d %H:%M:%S")

                # display the current time
                for l in range(len(mainWindow.active_labels)):
                    mainWindow.activation_status_list[mainWindow.active_labels[l]].setToolTip(select_time)


# setup GUI
app = QApplication(sys.argv)
mainWindow = MainWindow()
mainWindow.show()

sys.exit(app.exec_())
