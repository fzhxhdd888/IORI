# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_selectlossfile.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Window_selectlossfile(object):
    def setupUi(self, Window_selectlossfile):
        Window_selectlossfile.setObjectName("Window_selectlossfile")
        Window_selectlossfile.resize(844, 239)
        self.centralwidget = QtWidgets.QWidget(Window_selectlossfile)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(60, 20, 721, 144))
        self.widget.setObjectName("widget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.widget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit_CUlossfile = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_CUlossfile.setObjectName("lineEdit_CUlossfile")
        self.gridLayout.addWidget(self.lineEdit_CUlossfile, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_SAlossfile = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_SAlossfile.setObjectName("lineEdit_SAlossfile")
        self.gridLayout.addWidget(self.lineEdit_SAlossfile, 1, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEdit_ESGLOSS = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_ESGLOSS.setText("")
        self.lineEdit_ESGLOSS.setObjectName("lineEdit_ESGLOSS")
        self.gridLayout.addWidget(self.lineEdit_ESGLOSS, 2, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 2, 1)
        self.pushButton_ok = QtWidgets.QPushButton(self.widget)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.gridLayout_2.addWidget(self.pushButton_ok, 2, 1, 1, 1)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton_selectCUloss = QtWidgets.QPushButton(self.widget)
        self.pushButton_selectCUloss.setObjectName("pushButton_selectCUloss")
        self.verticalLayout_2.addWidget(self.pushButton_selectCUloss)
        self.pushButton_selectSAloss = QtWidgets.QPushButton(self.widget)
        self.pushButton_selectSAloss.setObjectName("pushButton_selectSAloss")
        self.verticalLayout_2.addWidget(self.pushButton_selectSAloss)
        self.pushButton_selectESGloss = QtWidgets.QPushButton(self.widget)
        self.pushButton_selectESGloss.setObjectName("pushButton_selectESGloss")
        self.verticalLayout_2.addWidget(self.pushButton_selectESGloss)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 1, 1, 1)
        Window_selectlossfile.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Window_selectlossfile)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 844, 26))
        self.menubar.setObjectName("menubar")
        Window_selectlossfile.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Window_selectlossfile)
        self.statusbar.setObjectName("statusbar")
        Window_selectlossfile.setStatusBar(self.statusbar)

        self.retranslateUi(Window_selectlossfile)
        QtCore.QMetaObject.connectSlotsByName(Window_selectlossfile)

    def retranslateUi(self, Window_selectlossfile):
        _translate = QtCore.QCoreApplication.translate
        Window_selectlossfile.setWindowTitle(_translate("Window_selectlossfile", "Select Loss File"))
        self.label.setText(_translate("Window_selectlossfile", "DUT -> CU:"))
        self.label_2.setText(_translate("Window_selectlossfile", "DUT -> SA:"))
        self.label_3.setText(_translate("Window_selectlossfile", "DUT -> ESG:"))
        self.pushButton_ok.setText(_translate("Window_selectlossfile", "OK"))
        self.pushButton_selectCUloss.setText(_translate("Window_selectlossfile", "Select Loss File"))
        self.pushButton_selectSAloss.setText(_translate("Window_selectlossfile", "Select Loss File"))
        self.pushButton_selectESGloss.setText(_translate("Window_selectlossfile", "Select Loss File"))

