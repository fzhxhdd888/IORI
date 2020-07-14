# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_NEWDUT.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewDUT(object):
    def setupUi(self, NewDUT):
        NewDUT.setObjectName("NewDUT")
        NewDUT.resize(529, 110)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("image/icon/dut.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        NewDUT.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(NewDUT)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(21, 20, 484, 30))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.lineEdit_dutname = QtWidgets.QLineEdit(self.layoutWidget)
        self.lineEdit_dutname.setObjectName("lineEdit_dutname")
        self.horizontalLayout.addWidget(self.lineEdit_dutname)
        self.pushButton_ok = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_ok.setObjectName("pushButton_ok")
        self.horizontalLayout.addWidget(self.pushButton_ok)
        self.pushButton_cancel = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        NewDUT.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(NewDUT)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 529, 26))
        self.menubar.setObjectName("menubar")
        NewDUT.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(NewDUT)
        self.statusbar.setObjectName("statusbar")
        NewDUT.setStatusBar(self.statusbar)

        self.retranslateUi(NewDUT)
        QtCore.QMetaObject.connectSlotsByName(NewDUT)

    def retranslateUi(self, NewDUT):
        _translate = QtCore.QCoreApplication.translate
        NewDUT.setWindowTitle(_translate("NewDUT", "New DUT"))
        self.label.setText(_translate("NewDUT", "New DUT Name:"))
        self.pushButton_ok.setText(_translate("NewDUT", "OK"))
        self.pushButton_cancel.setText(_translate("NewDUT", "Cancel"))

