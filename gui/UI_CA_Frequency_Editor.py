# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_CA_Frequency_Editor.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow_CA_Freq_Editor(object):
    def setupUi(self, MainWindow_CA_Freq_Editor):
        MainWindow_CA_Freq_Editor.setObjectName("MainWindow_CA_Freq_Editor")
        MainWindow_CA_Freq_Editor.resize(916, 640)
        self.centralwidget = QtWidgets.QWidget(MainWindow_CA_Freq_Editor)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.tableWidget_2C = QtWidgets.QTableWidget(self.tab)
        self.tableWidget_2C.setObjectName("tableWidget_2C")
        self.tableWidget_2C.setColumnCount(2)
        self.tableWidget_2C.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2C.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2C.setHorizontalHeaderItem(1, item)
        self.verticalLayout_2.addWidget(self.tableWidget_2C)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab_2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.tableWidget_5B = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget_5B.setObjectName("tableWidget_5B")
        self.tableWidget_5B.setColumnCount(2)
        self.tableWidget_5B.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_5B.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_5B.setHorizontalHeaderItem(1, item)
        self.horizontalLayout_3.addWidget(self.tableWidget_5B)
        self.tabWidget.addTab(self.tab_2, "")
        self.CA_7C = QtWidgets.QWidget()
        self.CA_7C.setObjectName("CA_7C")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.CA_7C)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tableWidget_7C = QtWidgets.QTableWidget(self.CA_7C)
        self.tableWidget_7C.setObjectName("tableWidget_7C")
        self.tableWidget_7C.setColumnCount(2)
        self.tableWidget_7C.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_7C.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_7C.setHorizontalHeaderItem(1, item)
        self.horizontalLayout_4.addWidget(self.tableWidget_7C)
        self.tabWidget.addTab(self.CA_7C, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.tab_3)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.tableWidget_12B = QtWidgets.QTableWidget(self.tab_3)
        self.tableWidget_12B.setObjectName("tableWidget_12B")
        self.tableWidget_12B.setColumnCount(2)
        self.tableWidget_12B.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_12B.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_12B.setHorizontalHeaderItem(1, item)
        self.horizontalLayout_5.addWidget(self.tableWidget_12B)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.tab_4)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.tableWidget_38C = QtWidgets.QTableWidget(self.tab_4)
        self.tableWidget_38C.setObjectName("tableWidget_38C")
        self.tableWidget_38C.setColumnCount(2)
        self.tableWidget_38C.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_38C.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_38C.setHorizontalHeaderItem(1, item)
        self.horizontalLayout_6.addWidget(self.tableWidget_38C)
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.tab_5)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.tableWidget_41C = QtWidgets.QTableWidget(self.tab_5)
        self.tableWidget_41C.setObjectName("tableWidget_41C")
        self.tableWidget_41C.setColumnCount(2)
        self.tableWidget_41C.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_41C.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_41C.setHorizontalHeaderItem(1, item)
        self.horizontalLayout_7.addWidget(self.tableWidget_41C)
        self.tabWidget.addTab(self.tab_5, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.pushButton_setdefaultvalue = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_setdefaultvalue.setObjectName("pushButton_setdefaultvalue")
        self.verticalLayout.addWidget(self.pushButton_setdefaultvalue)
        self.pushButton_ok = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.verticalLayout.addWidget(self.pushButton_ok)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        MainWindow_CA_Freq_Editor.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow_CA_Freq_Editor)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 916, 26))
        self.menubar.setObjectName("menubar")
        MainWindow_CA_Freq_Editor.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow_CA_Freq_Editor)
        self.statusbar.setObjectName("statusbar")
        MainWindow_CA_Freq_Editor.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow_CA_Freq_Editor)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow_CA_Freq_Editor)

    def retranslateUi(self, MainWindow_CA_Freq_Editor):
        _translate = QtCore.QCoreApplication.translate
        MainWindow_CA_Freq_Editor.setWindowTitle(_translate("MainWindow_CA_Freq_Editor", "MainWindow"))
        item = self.tableWidget_2C.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow_CA_Freq_Editor", "Bandwidth"))
        item = self.tableWidget_2C.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow_CA_Freq_Editor", " Channel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow_CA_Freq_Editor", "CA_2C"))
        item = self.tableWidget_5B.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow_CA_Freq_Editor", "Bandwidth"))
        item = self.tableWidget_5B.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow_CA_Freq_Editor", " Channel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow_CA_Freq_Editor", "CA_5B"))
        item = self.tableWidget_7C.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow_CA_Freq_Editor", "New Column"))
        item = self.tableWidget_7C.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow_CA_Freq_Editor", "Bandwidth"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.CA_7C), _translate("MainWindow_CA_Freq_Editor", "CA_7C"))
        item = self.tableWidget_12B.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow_CA_Freq_Editor", "New Column"))
        item = self.tableWidget_12B.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow_CA_Freq_Editor", "Bandwidth"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow_CA_Freq_Editor", "CA_12B"))
        item = self.tableWidget_38C.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow_CA_Freq_Editor", "New Column"))
        item = self.tableWidget_38C.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow_CA_Freq_Editor", "Bandwidth"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow_CA_Freq_Editor", "CA_38C"))
        item = self.tableWidget_41C.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow_CA_Freq_Editor", "New Column"))
        item = self.tableWidget_41C.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow_CA_Freq_Editor", "Bandwidth"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow_CA_Freq_Editor", "CA_41C"))
        self.pushButton_setdefaultvalue.setText(_translate("MainWindow_CA_Freq_Editor", "Set to Default Value"))
        self.pushButton_ok.setText(_translate("MainWindow_CA_Freq_Editor", "OK"))
