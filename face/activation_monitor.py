# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'activation_monitor.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 480)
        MainWindow.setMinimumSize(QtCore.QSize(640, 480))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ico.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.manual_load_data = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(True)
        font.setWeight(75)
        self.manual_load_data.setFont(font)
        self.manual_load_data.setObjectName("manual_load_data")
        self.horizontalLayout.addWidget(self.manual_load_data)
        self.reload = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(True)
        font.setWeight(75)
        self.reload.setFont(font)
        self.reload.setObjectName("reload")
        self.horizontalLayout.addWidget(self.reload)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 3, 1, 1)
        self.mac_type_select = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(True)
        font.setWeight(75)
        self.mac_type_select.setFont(font)
        self.mac_type_select.setObjectName("mac_type_select")
        self.mac_type_select.addItem("")
        self.mac_type_select.addItem("")
        self.mac_type_select.addItem("")
        self.mac_type_select.addItem("")
        self.mac_type_select.addItem("")
        self.mac_type_select.addItem("")
        self.mac_type_select.addItem("")
        self.mac_type_select.addItem("")
        self.gridLayout_2.addWidget(self.mac_type_select, 0, 1, 1, 1)
        self.category_select = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(True)
        font.setWeight(75)
        self.category_select.setFont(font)
        self.category_select.setObjectName("category_select")
        self.category_select.addItem("")
        self.category_select.addItem("")
        self.category_select.addItem("")
        self.category_select.addItem("")
        self.category_select.addItem("")
        self.category_select.addItem("")
        self.category_select.addItem("")
        self.category_select.addItem("")
        self.category_select.addItem("")
        self.gridLayout_2.addWidget(self.category_select, 0, 0, 1, 1)
        self.from_time = QtWidgets.QDateTimeEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(True)
        font.setWeight(75)
        self.from_time.setFont(font)
        self.from_time.setDateTime(QtCore.QDateTime(QtCore.QDate(2018, 4, 1), QtCore.QTime(0, 0, 0)))
        self.from_time.setCalendarPopup(True)
        self.from_time.setObjectName("from_time")
        self.gridLayout_2.addWidget(self.from_time, 1, 0, 1, 1)
        self.to_time = QtWidgets.QDateTimeEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(True)
        font.setWeight(75)
        self.to_time.setFont(font)
        self.to_time.setDateTime(QtCore.QDateTime(QtCore.QDate(2018, 4, 2), QtCore.QTime(0, 0, 0)))
        self.to_time.setCalendarPopup(True)
        self.to_time.setObjectName("to_time")
        self.gridLayout_2.addWidget(self.to_time, 1, 1, 1, 1)
        self.auto_load_data = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.auto_load_data.setFont(font)
        self.auto_load_data.setObjectName("auto_load_data")
        self.gridLayout_2.addWidget(self.auto_load_data, 0, 3, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_mac_no_example = QtWidgets.QLabel(self.centralwidget)
        self.label_mac_no_example.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.label_mac_no_example.setFont(font)
        self.label_mac_no_example.setObjectName("label_mac_no_example")
        self.horizontalLayout_3.addWidget(self.label_mac_no_example)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.from_time_stamp = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.from_time_stamp.setFont(font)
        self.from_time_stamp.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.from_time_stamp.setObjectName("from_time_stamp")
        self.horizontalLayout_3.addWidget(self.from_time_stamp)
        self.label_activation_status_example = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.label_activation_status_example.setFont(font)
        self.label_activation_status_example.setAlignment(QtCore.Qt.AlignCenter)
        self.label_activation_status_example.setObjectName("label_activation_status_example")
        self.horizontalLayout_3.addWidget(self.label_activation_status_example)
        self.to_time_stamp = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(6)
        font.setBold(True)
        font.setWeight(75)
        self.to_time_stamp.setFont(font)
        self.to_time_stamp.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.to_time_stamp.setObjectName("to_time_stamp")
        self.horizontalLayout_3.addWidget(self.to_time_stamp)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setText("")
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.label_yield_val_example = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.label_yield_val_example.setFont(font)
        self.label_yield_val_example.setAlignment(QtCore.Qt.AlignCenter)
        self.label_yield_val_example.setObjectName("label_yield_val_example")
        self.horizontalLayout_3.addWidget(self.label_yield_val_example)
        self.label_activation_val_example = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.label_activation_val_example.setFont(font)
        self.label_activation_val_example.setAlignment(QtCore.Qt.AlignCenter)
        self.label_activation_val_example.setObjectName("label_activation_val_example")
        self.horizontalLayout_3.addWidget(self.label_activation_val_example)
        self.horizontalLayout_3.setStretch(0, 1)
        self.horizontalLayout_3.setStretch(3, 9)
        self.horizontalLayout_3.setStretch(6, 1)
        self.horizontalLayout_3.setStretch(7, 1)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setEnabled(True)
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setBold(True)
        font.setWeight(75)
        self.scrollArea.setFont(font)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 601, 310))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setColumnStretch(0, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_2.addWidget(self.scrollArea)
        self.verticalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 9)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.category_select.setCurrentIndex(5)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GFC Activation Monitor produced by Carl.Cheung"))
        self.manual_load_data.setText(_translate("MainWindow", "Manual Load"))
        self.reload.setText(_translate("MainWindow", "Reload Data"))
        self.mac_type_select.setItemText(0, _translate("MainWindow", "GFC-UP"))
        self.mac_type_select.setItemText(1, _translate("MainWindow", "GFC-DOWN"))
        self.mac_type_select.setItemText(2, _translate("MainWindow", "OQC-UP"))
        self.mac_type_select.setItemText(3, _translate("MainWindow", "OQC-DOWN"))
        self.mac_type_select.setItemText(4, _translate("MainWindow", "REL-UP"))
        self.mac_type_select.setItemText(5, _translate("MainWindow", "REL-DOWN"))
        self.mac_type_select.setItemText(6, _translate("MainWindow", "CUBE-UP"))
        self.mac_type_select.setItemText(7, _translate("MainWindow", "CUBE-DOWN"))
        self.category_select.setItemText(0, _translate("MainWindow", "Syrup-A"))
        self.category_select.setItemText(1, _translate("MainWindow", "Syrup-S"))
        self.category_select.setItemText(2, _translate("MainWindow", "Lumber"))
        self.category_select.setItemText(3, _translate("MainWindow", "Granite-C"))
        self.category_select.setItemText(4, _translate("MainWindow", "Granite-D"))
        self.category_select.setItemText(5, _translate("MainWindow", "Granite-E"))
        self.category_select.setItemText(6, _translate("MainWindow", "BlueBerry"))
        self.category_select.setItemText(7, _translate("MainWindow", "Angel-P"))
        self.category_select.setItemText(8, _translate("MainWindow", "Angel-R"))
        self.from_time.setDisplayFormat(_translate("MainWindow", "yyyy/M/d H:mm:ss"))
        self.to_time.setDisplayFormat(_translate("MainWindow", "yyyy/M/d H:mm:ss"))
        self.auto_load_data.setText(_translate("MainWindow", "Show Today"))
        self.label_mac_no_example.setText(_translate("MainWindow", "Machine No."))
        self.from_time_stamp.setText(_translate("MainWindow", "00:00"))
        self.label_activation_status_example.setText(_translate("MainWindow", "Activation Status"))
        self.to_time_stamp.setText(_translate("MainWindow", "24:00"))
        self.label_yield_val_example.setText(_translate("MainWindow", "Yield"))
        self.label_activation_val_example.setText(_translate("MainWindow", "Activation Value"))

