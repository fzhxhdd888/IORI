# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_devices_config.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Scan_Devices(object):
    def setupUi(self, Scan_Devices):
        Scan_Devices.setObjectName("Scan_Devices")
        Scan_Devices.resize(909, 657)
        Scan_Devices.setSizeIncrement(QtCore.QSize(3, 3))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("image/icon/device.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Scan_Devices.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(Scan_Devices)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial Unicode MS")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.comboBox_SA_AddrType = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_SA_AddrType.setObjectName("comboBox_SA_AddrType")
        self.comboBox_SA_AddrType.addItem("")
        self.comboBox_SA_AddrType.addItem("")
        self.gridLayout.addWidget(self.comboBox_SA_AddrType, 2, 3, 1, 1)
        self.comboBox_CU_AddrType = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_CU_AddrType.setObjectName("comboBox_CU_AddrType")
        self.comboBox_CU_AddrType.addItem("")
        self.comboBox_CU_AddrType.addItem("")
        self.gridLayout.addWidget(self.comboBox_CU_AddrType, 1, 3, 1, 1)
        self.comboBox_ESG_AddrType = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_ESG_AddrType.setObjectName("comboBox_ESG_AddrType")
        self.comboBox_ESG_AddrType.addItem("")
        self.comboBox_ESG_AddrType.addItem("")
        self.gridLayout.addWidget(self.comboBox_ESG_AddrType, 3, 3, 1, 1)
        self.comboBox_PSG_AddrType = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_PSG_AddrType.setObjectName("comboBox_PSG_AddrType")
        self.comboBox_PSG_AddrType.addItem("")
        self.comboBox_PSG_AddrType.addItem("")
        self.gridLayout.addWidget(self.comboBox_PSG_AddrType, 4, 3, 1, 1)
        self.comboBox_PS_AddrType = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_PS_AddrType.setObjectName("comboBox_PS_AddrType")
        self.comboBox_PS_AddrType.addItem("")
        self.comboBox_PS_AddrType.addItem("")
        self.gridLayout.addWidget(self.comboBox_PS_AddrType, 5, 3, 1, 1)
        self.comboBox_SU_AddrType = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_SU_AddrType.setObjectName("comboBox_SU_AddrType")
        self.comboBox_SU_AddrType.addItem("")
        self.comboBox_SU_AddrType.addItem("")
        self.gridLayout.addWidget(self.comboBox_SU_AddrType, 6, 3, 1, 1)
        self.checkBox_PSG = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(17)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_PSG.sizePolicy().hasHeightForWidth())
        self.checkBox_PSG.setSizePolicy(sizePolicy)
        self.checkBox_PSG.setMinimumSize(QtCore.QSize(16, 16))
        self.checkBox_PSG.setMaximumSize(QtCore.QSize(16, 16))
        self.checkBox_PSG.setText("")
        self.checkBox_PSG.setObjectName("checkBox_PSG")
        self.gridLayout.addWidget(self.checkBox_PSG, 4, 0, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 0, 3, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 0, 2, 1, 1)
        self.lineEdit_SU_Addr = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_SU_Addr.setObjectName("lineEdit_SU_Addr")
        self.gridLayout.addWidget(self.lineEdit_SU_Addr, 6, 4, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 1, 1, 1)
        self.lineEdit_PSG_Addr = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_PSG_Addr.setObjectName("lineEdit_PSG_Addr")
        self.gridLayout.addWidget(self.lineEdit_PSG_Addr, 4, 4, 1, 1)
        self.comboBox_CU_Name = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_CU_Name.setObjectName("comboBox_CU_Name")
        self.comboBox_CU_Name.addItem("")
        self.comboBox_CU_Name.addItem("")
        self.comboBox_CU_Name.addItem("")
        self.gridLayout.addWidget(self.comboBox_CU_Name, 1, 2, 1, 1)
        self.lineEdit_CU_Addr = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_CU_Addr.setObjectName("lineEdit_CU_Addr")
        self.gridLayout.addWidget(self.lineEdit_CU_Addr, 1, 4, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 0, 1, 1, 1)
        self.lineEdit_SA_Addr = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_SA_Addr.setObjectName("lineEdit_SA_Addr")
        self.gridLayout.addWidget(self.lineEdit_SA_Addr, 2, 4, 1, 1)
        self.checkBox_PS = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(17)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_PS.sizePolicy().hasHeightForWidth())
        self.checkBox_PS.setSizePolicy(sizePolicy)
        self.checkBox_PS.setMinimumSize(QtCore.QSize(16, 16))
        self.checkBox_PS.setMaximumSize(QtCore.QSize(16, 16))
        self.checkBox_PS.setText("")
        self.checkBox_PS.setObjectName("checkBox_PS")
        self.gridLayout.addWidget(self.checkBox_PS, 5, 0, 1, 1)
        self.checkBox_SA = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(17)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_SA.sizePolicy().hasHeightForWidth())
        self.checkBox_SA.setSizePolicy(sizePolicy)
        self.checkBox_SA.setMinimumSize(QtCore.QSize(16, 16))
        self.checkBox_SA.setMaximumSize(QtCore.QSize(16, 16))
        self.checkBox_SA.setText("")
        self.checkBox_SA.setObjectName("checkBox_SA")
        self.gridLayout.addWidget(self.checkBox_SA, 2, 0, 1, 1)
        self.checkBox_SU = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(17)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_SU.sizePolicy().hasHeightForWidth())
        self.checkBox_SU.setSizePolicy(sizePolicy)
        self.checkBox_SU.setMinimumSize(QtCore.QSize(16, 16))
        self.checkBox_SU.setMaximumSize(QtCore.QSize(16, 16))
        self.checkBox_SU.setText("")
        self.checkBox_SU.setObjectName("checkBox_SU")
        self.gridLayout.addWidget(self.checkBox_SU, 6, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 0, 4, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)
        self.comboBox_SA_Name = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_SA_Name.setObjectName("comboBox_SA_Name")
        self.comboBox_SA_Name.addItem("")
        self.comboBox_SA_Name.addItem("")
        self.gridLayout.addWidget(self.comboBox_SA_Name, 2, 2, 1, 1)
        self.checkBox_ESG = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(17)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_ESG.sizePolicy().hasHeightForWidth())
        self.checkBox_ESG.setSizePolicy(sizePolicy)
        self.checkBox_ESG.setMinimumSize(QtCore.QSize(16, 16))
        self.checkBox_ESG.setMaximumSize(QtCore.QSize(16, 16))
        self.checkBox_ESG.setText("")
        self.checkBox_ESG.setObjectName("checkBox_ESG")
        self.gridLayout.addWidget(self.checkBox_ESG, 3, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 1, 1, 1)
        self.comboBox_PS_Name = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_PS_Name.setObjectName("comboBox_PS_Name")
        self.comboBox_PS_Name.addItem("")
        self.gridLayout.addWidget(self.comboBox_PS_Name, 5, 2, 1, 1)
        self.lineEdit_PS_Addr = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_PS_Addr.setObjectName("lineEdit_PS_Addr")
        self.gridLayout.addWidget(self.lineEdit_PS_Addr, 5, 4, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 0, 0, 1, 1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 1, 1, 1)
        self.lineEdit_ESG_Addr = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_ESG_Addr.setObjectName("lineEdit_ESG_Addr")
        self.gridLayout.addWidget(self.lineEdit_ESG_Addr, 3, 4, 1, 1)
        self.comboBox_ESG_Name = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_ESG_Name.setObjectName("comboBox_ESG_Name")
        self.gridLayout.addWidget(self.comboBox_ESG_Name, 3, 2, 1, 1)
        self.comboBox_PSG_Name = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_PSG_Name.setObjectName("comboBox_PSG_Name")
        self.gridLayout.addWidget(self.comboBox_PSG_Name, 4, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 6, 1, 1, 1)
        self.comboBox_SU_Name = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_SU_Name.setObjectName("comboBox_SU_Name")
        self.gridLayout.addWidget(self.comboBox_SU_Name, 6, 2, 1, 1)
        self.checkBox_CU = QtWidgets.QCheckBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(17)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_CU.sizePolicy().hasHeightForWidth())
        self.checkBox_CU.setSizePolicy(sizePolicy)
        self.checkBox_CU.setMinimumSize(QtCore.QSize(16, 16))
        self.checkBox_CU.setMaximumSize(QtCore.QSize(16, 16))
        self.checkBox_CU.setText("")
        self.checkBox_CU.setObjectName("checkBox_CU")
        self.gridLayout.addWidget(self.checkBox_CU, 1, 0, 1, 1)
        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setRowStretch(0, 100)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_Save = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Save.setObjectName("pushButton_Save")
        self.horizontalLayout.addWidget(self.pushButton_Save)
        self.pushButton_Cancel = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_Cancel.setObjectName("pushButton_Cancel")
        self.horizontalLayout.addWidget(self.pushButton_Cancel)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_scandevice = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_scandevice.setObjectName("pushButton_scandevice")
        self.horizontalLayout_3.addWidget(self.pushButton_scandevice)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.tableWidget_scandevice = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget_scandevice.setObjectName("tableWidget_scandevice")
        self.tableWidget_scandevice.setColumnCount(2)
        self.tableWidget_scandevice.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_scandevice.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_scandevice.setHorizontalHeaderItem(1, item)
        self.verticalLayout.addWidget(self.tableWidget_scandevice)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem5 = QtWidgets.QSpacerItem(20, 5, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout_2.addItem(spacerItem5)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        spacerItem6 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem6)
        Scan_Devices.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Scan_Devices)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 909, 26))
        self.menubar.setObjectName("menubar")
        Scan_Devices.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Scan_Devices)
        self.statusbar.setObjectName("statusbar")
        Scan_Devices.setStatusBar(self.statusbar)

        self.retranslateUi(Scan_Devices)
        self.pushButton_Cancel.clicked.connect(Scan_Devices.close)
        QtCore.QMetaObject.connectSlotsByName(Scan_Devices)

    def retranslateUi(self, Scan_Devices):
        _translate = QtCore.QCoreApplication.translate
        Scan_Devices.setWindowTitle(_translate("Scan_Devices", "Devices Config"))
        self.label_2.setText(_translate("Scan_Devices", "Address Config of Devices: "))
        self.comboBox_SA_AddrType.setItemText(0, _translate("Scan_Devices", "TCPIP"))
        self.comboBox_SA_AddrType.setItemText(1, _translate("Scan_Devices", "GPIB"))
        self.comboBox_CU_AddrType.setItemText(0, _translate("Scan_Devices", "GPIB"))
        self.comboBox_CU_AddrType.setItemText(1, _translate("Scan_Devices", "TCPIP"))
        self.comboBox_ESG_AddrType.setItemText(0, _translate("Scan_Devices", "GPIB"))
        self.comboBox_ESG_AddrType.setItemText(1, _translate("Scan_Devices", "TCPIP"))
        self.comboBox_PSG_AddrType.setItemText(0, _translate("Scan_Devices", "GPIB"))
        self.comboBox_PSG_AddrType.setItemText(1, _translate("Scan_Devices", "TCPIP"))
        self.comboBox_PS_AddrType.setItemText(0, _translate("Scan_Devices", "GPIB"))
        self.comboBox_PS_AddrType.setItemText(1, _translate("Scan_Devices", "TCPIP"))
        self.comboBox_SU_AddrType.setItemText(0, _translate("Scan_Devices", "GPIB"))
        self.comboBox_SU_AddrType.setItemText(1, _translate("Scan_Devices", "TCPIP"))
        self.label_11.setText(_translate("Scan_Devices", "Address Type"))
        self.label_10.setText(_translate("Scan_Devices", "Devices Name"))
        self.label_5.setText(_translate("Scan_Devices", "PSG"))
        self.comboBox_CU_Name.setItemText(0, _translate("Scan_Devices", "CMW500"))
        self.comboBox_CU_Name.setItemText(1, _translate("Scan_Devices", "CMU200"))
        self.comboBox_CU_Name.setItemText(2, _translate("Scan_Devices", "CBT"))
        self.lineEdit_CU_Addr.setText(_translate("Scan_Devices", "20"))
        self.label_9.setText(_translate("Scan_Devices", "Devices SN"))
        self.lineEdit_SA_Addr.setText(_translate("Scan_Devices", "192.168.1.10"))
        self.label_12.setText(_translate("Scan_Devices", "Address"))
        self.label_3.setText(_translate("Scan_Devices", "SA"))
        self.comboBox_SA_Name.setItemText(0, _translate("Scan_Devices", "FSQ"))
        self.comboBox_SA_Name.setItemText(1, _translate("Scan_Devices", "FSU"))
        self.label_4.setText(_translate("Scan_Devices", "ESG"))
        self.comboBox_PS_Name.setItemText(0, _translate("Scan_Devices", "E3632A"))
        self.label_8.setText(_translate("Scan_Devices", "Check"))
        self.label.setText(_translate("Scan_Devices", "CU"))
        self.label_6.setText(_translate("Scan_Devices", "PS"))
        self.label_7.setText(_translate("Scan_Devices", "SU"))
        self.pushButton_Save.setText(_translate("Scan_Devices", "Save"))
        self.pushButton_Cancel.setText(_translate("Scan_Devices", "Cancel"))
        self.pushButton_scandevice.setText(_translate("Scan_Devices", "Scan Devices"))
        item = self.tableWidget_scandevice.horizontalHeaderItem(0)
        item.setText(_translate("Scan_Devices", "Devices IDN"))
        item = self.tableWidget_scandevice.horizontalHeaderItem(1)
        item.setText(_translate("Scan_Devices", "Devices Address"))
